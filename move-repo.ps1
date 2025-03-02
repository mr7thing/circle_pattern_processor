# 仓库迁移脚本
# 此脚本用于将Git仓库从上级目录迁移到当前目录

# 步骤1: 在当前目录初始化新的Git仓库
Write-Host "在当前目录初始化新的Git仓库..."
git init

# 步骤2: 添加所有文件到新仓库
Write-Host "添加文件到Git仓库..."
git add .

# 步骤3: 提交更改
Write-Host "提交第一次更改..."
git commit -m "chore: 将仓库迁移到子目录"

# 步骤4: 从原始仓库获取提交历史（可选）
Write-Host "如果需要保留完整的提交历史，请执行以下步骤："
Write-Host "1. 添加原始仓库作为远程仓库："
Write-Host "   git remote add original ../../.."
Write-Host "2. 拉取原始仓库的历史："
Write-Host "   git fetch original"
Write-Host "3. 合并历史（可能需要解决冲突）："
Write-Host "   git merge original/master --allow-unrelated-histories"

# 步骤5: 如果有远程仓库，设置新的远程仓库
Write-Host "如果需要设置远程仓库，请执行："
Write-Host "git remote add origin YOUR_REMOTE_URL"
Write-Host "git push -u origin master"

Write-Host "仓库迁移完成！现在您可以在当前目录中使用Git管理代码了。"