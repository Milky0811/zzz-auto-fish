---

# zzz-auto-fish

基于图像识别的绝区零赛博钓鱼脚本。  
下载后直接运行 `近岸.py` 和 `石礁.py` 即可在对应的区域自动钓鱼。
B站展示链接
https://www.bilibili.com/video/BV1k8ApeaELT/ 

---

## 项目简介

`zzz-auto-fish` 是一个基于图像识别技术的自动化钓鱼脚本，专为绝区零游戏设计。通过捕捉游戏画面中的特定元素，脚本可以自动完成钓鱼操作，支持近岸和石礁两种钓鱼区域。

---

## 快速开始

### 环境要求

- **Python 版本**: 3.12（推荐）
- **依赖库**: 请确保安装 `requirements.txt` 中列出的所有依赖。

### 安装依赖

1. 克隆本仓库到本地：（直接打包下载我的也行）
   ```bash
   git clone https://github.com/your-repo(改成你自己的fork仓库)/zzz-auto-fish.git
   cd zzz-auto-fish
   ```
2. 安装依赖：（也可以直接运行，报错后将信息丢给ai，他会提示你要装什么库）
   ```bash
   pip install -r requirements.txt
   ```

### 运行脚本

- **近岸区域钓鱼**：
  ```bash
  python 近岸.py
  ```
- **石礁区域钓鱼**：
  ```bash
  python 石礁.py
  ```


## 使用说明

1. **确保游戏窗口在前台**：脚本依赖于屏幕截图，因此游戏窗口必须处于前台且不被遮挡。
2. **运行脚本**：根据钓鱼区域选择运行 `近岸.py` 或 `石礁.py`。
3. **结束脚本**：脚本运行时，任意窗口按esc即可退出

---

## 注意事项

- **Python 版本**：建议使用 Python 3.12，其他版本可能不兼容。
- 代码里这部分估计是需要改的： 设置区域 left, top, right, bottom = 2060, 1100, 2210, 1250。 
- 因为我的屏幕是2560*1440，每个人的显示大小可能不同，识别的位置自然有区别，欢迎大家给出不同分辨率的参数
- 因为用的是灰度图，电脑开了HDR的话会过曝，记得关下
---

## 问题反馈

如果在使用过程中遇到问题，请联系：  
**邮箱**: 3042463091@qq.com

---

## 免责声明

本项目仅供学习和研究使用，请勿用于任何商业或非法用途。使用本脚本产生的一切后果由使用者自行承担。

---

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

---
