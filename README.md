# MB Average 自动更新网页版（三年）

## 一次性部署：GitHub Pages（公开网页）
1. 登录 GitHub，新建 **Public** repository，例如 `mb-average`。
2. 上传本 ZIP 解压后的所有文件，**包括隐藏的 `.github/workflows/update.yml`**。
3. 仓库 Settings → Pages → Build and deployment → Source 选 **Deploy from a branch**；Branch 选 `main`、`/(root)`，保存。
4. Actions → `Update FX daily ranges` → `Run workflow`，首次生成 `data.json`。确认 Action 成功后等待 Pages 部署。
5. 访问 `https://你的GitHub用户名.github.io/mb-average/`，在 iPhone Safari 添加到主屏幕。

之后 GitHub Actions 按 UTC 01:20（新加坡时间 09:20）周二至周六尝试更新；GitHub 的定时任务可能延迟或暂停。网页本身不需要电脑 MT5。

## 注意
- 行情来自 Yahoo Finance 的非官方数据接口（yfinance），不保证长期稳定或 28 对全部可用。失败时沿用上次数据并标记 stale；首次失败显示不可用，**绝不使用假数据**。
- 数据以 Yahoo 提供的 D1 K 线为准，日线切分、价格精度和 Tradehall MT5 可能不同；本方案按非日元 0.00001、日元 0.001 定义 point。
- `Top 5 average` 是三年内最大五根已收盘 D1 的 High-Low 点数均值；`建议布局` 是其一半，不是保证有效的止损距离。
- 免费公开 GitHub Pages 的页面和 data.json 对所有人可见；不应上传 MT5 账号、密码、交易记录或其他敏感资料。
- 若 Github 的免费政策或 Yahoo 接口变化，自动更新可能需要调整。
