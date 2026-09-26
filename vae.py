"""从《Diffusion 从入门到精通》第三章 VAE 推导对应的工程接口。

书上的符号 -> 工程代码:
  phi (推断模型参数)            -> self.encoder 的参数
  theta (生成模型参数)          -> self.decoder 的参数
  q_phi(z|x) = N(mu, sigma^2)   -> encoder.forward 返回 (mu, logvar)
  z = mu + sigma * epsilon       -> reparameterize(mu, logvar)
  p_theta(x|z) (decoder)        -> decoder.forward(z)
  E_q[log p_theta(x|z)]         -> reconstruction_loss (MSE / BCE)
  D_KL(q_phi(z|x) || p_theta(z))-> kl_divergence
  ELBO                          -> elbo_loss
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):
    """推断模型 q_phi(z|x) —— 对应书上的参数 phi。

    输入图 x，输出隐变量高斯的均值 mu 和"对数方差" logvar。
    即 q_phi(z|x) = N(z; mu_phi(x), diag(sigma_phi^2(x)))。
    注意：输出的是分布（mu, logvar），不是一个点。
    """

    def __init__(self, input_dim, hidden_dims, latent_dim):
        super().__init__()
        layers = []
        prev = input_dim
        for h in hidden_dims:
            layers += [nn.Linear(prev, h), nn.ReLU()]
            prev = h
        self.backbone = nn.Sequential(*layers)
        self.fc_mu = nn.Linear(prev, latent_dim)      # mu_phi(x)
        self.fc_logvar = nn.Linear(prev, latent_dim)  # log sigma_phi^2(x)

    def forward(self, x):
        h = self.backbone(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar


class Decoder(nn.Module):
    """生成模型 p_theta(x|z) —— 对应书上的参数 theta。

    输入隐变量 z，输出重建 x_hat（高斯 decoder 的均值）。
    """

    def __init__(self, latent_dim, hidden_dims, output_dim):
        super().__init__()
        layers = []
        prev = latent_dim
        for h in hidden_dims:
            layers += [nn.Linear(prev, h), nn.ReLU()]
            prev = h
        self.backbone = nn.Sequential(*layers)
        self.fc_out = nn.Linear(prev, output_dim)  # x_hat
        # 连续像素: 直接输出 + MSE
        # 二值像素(0/1): 后面接 Sigmoid + BCE

    def forward(self, z):
        return self.fc_out(self.backbone(z))


class VAE(nn.Module):
    """完整 VAE：两套参数 phi/theta 被同一个 ELBO 目标一起训练。"""

    def __init__(self, input_dim, hidden_dims, latent_dim):
        super().__init__()
        self.latent_dim = latent_dim
        self.encoder = Encoder(input_dim, hidden_dims, latent_dim)          # phi
        self.decoder = Decoder(latent_dim, hidden_dims[::-1], input_dim)    # theta

    def reparameterize(self, mu, logvar):
        """重参数化技巧：z = mu + sigma * epsilon, epsilon ~ N(0, I)。

        这样采样操作变成可微的，梯度能流回 encoder 的 phi。
        """
        std = torch.exp(0.5 * logvar)   # sigma = exp(0.5 * logvar)
        eps = torch.randn_like(std)     # epsilon ~ N(0, I)
        return mu + std * eps

    def forward(self, x):
        """训练流程：x -> q_phi(z|x) -> z -> p_theta(x|z) -> x_hat."""
        mu, logvar = self.encoder(x)          # 1. encode：得 q_phi(z|x)
        z = self.reparameterize(mu, logvar)   # 2. 可微采样 z
        x_hat = self.decoder(z)               # 3. decode：重建
        return x_hat, mu, logvar

    def kl_divergence(self, mu, logvar):
        """D_KL(q_phi(z|x) || p_theta(z))，其中 p_theta(z) = N(0, I)。

        对角高斯对标准高斯的 KL 有解析解，无需采样/积分：
        -0.5 * sum(1 + logvar - mu^2 - exp(logvar))
        """
        return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp(), dim=1)

    def reconstruction_loss(self, x, x_hat):
        """-E_q[log p_theta(x|z)]。

        高斯 decoder（固定方差）时，最大化 log p_theta(x|z) 等价于最小化 MSE。
        """
        return F.mse_loss(x_hat, x, reduction="sum") / x.size(0)
        # 二值图像时换成:
        # return F.binary_cross_entropy_with_logits(x_hat, x, reduction="sum") / x.size(0)

    def elbo_loss(self, x):
        """loss = -ELBO = reconstruction + KL。

        最小化它 = 最大化书上的 ELBO；同一个 loss 会同时更新 phi 和 theta。
        """
        x_hat, mu, logvar = self.forward(x)
        recon = self.reconstruction_loss(x, x_hat)
        kl = self.kl_divergence(mu, logvar).mean()
        return recon + kl, recon, kl

    @torch.no_grad()
    def sample(self, num_samples, device):
        """训练完成后的生成流程（不再用 encoder）：
        z ~ p_theta(z) = N(0, I) -> decoder -> 新图片。
        """
        z = torch.randn(num_samples, self.latent_dim, device=device)
        return self.decoder(z)


if __name__ == "__main__":
    # 示例：MNIST 28x28 -> 784 维
    input_dim = 784
    hidden_dims = [512, 256]
    latent_dim = 32

    model = VAE(input_dim=input_dim, hidden_dims=hidden_dims, latent_dim=latent_dim)
    print(model)

    # 模拟一个 batch
    x = torch.randn(16, input_dim)
    x_hat, mu, logvar = model(x)
    print(f"x shape:      {x.shape}")
    print(f"x_hat shape:  {x_hat.shape}")
    print(f"mu shape:     {mu.shape}")
    print(f"logvar shape: {logvar.shape}")

    loss, recon, kl = model.elbo_loss(x)
    print(f"total loss: {loss.item():.4f}")
    print(f"recon term: {recon.item():.4f}")
    print(f"kl term:    {kl.item():.4f}")

    # 生成新图片：只走 decoder，从先验 N(0, I) 采样
    samples = model.sample(8, device=torch.device("cpu"))
    print(f"generated samples shape: {samples.shape}")
