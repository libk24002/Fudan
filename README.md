# C 语言练习与 AI 归档平台

## 项目简介

本仓库用于 C 语言与算法练习，新增了本地单用户平台能力：

- 提交题目并进入练题会话
- 在沙箱中执行 C/C++/Java 代码
- 提交用户思路并触发 AI 评审
- 通过 `确认结束` + `归档入库` 两按钮完成自动收录
- 自动生成检索索引（按模块、按 C 技术点）
- AI 评审输出结构化评分（正确性、复杂度、边界条件、代码质量、思路清晰度）
- 前端展示评审历史评分趋势（同题多次评审）
- 前端提供历史评分折线图（总分趋势可视化）

## 技术栈

- **后端**: Python + FastAPI
- **前端**: React + Vite + Vitest
- **沙箱**: Docker（默认 runsc，可回退 runc）
- **练习代码**: C (C11 标准)

## 项目结构

```
Fudan/
├── Exercise/                            # 原有 C 练习代码
├── apps/
│   ├── api/                             # FastAPI 后端（题目/练题/评审/归档）
│   └── web/                             # 本地 Web 页面
├── problems/                            # 自动归档后的题目目录
├── index/                               # 自动生成索引
├── infra/sandbox/                       # 沙箱镜像与安全文档
├── docs/superpowers/specs/              # 设计文档
├── docs/superpowers/plans/              # 实施计划
├── scripts/check.sh                     # 后端+前端+沙箱检查脚本
├── main.c
├── CMakeLists.txt
└── .gitignore
```

## 后端能力概览

- `POST /api/problems`：创建练题会话
- `POST /api/sandbox/execute`：沙箱执行（C/C++/Java）
- `POST /api/problems/{id}/submit`：提交代码与思路
- `POST /api/problems/{id}/finish`：确认结束
- `POST /api/problems/{id}/review`：AI 评审
- `POST /api/problems/{id}/archive`：归档入库

## 自动归档产物

归档后每题写入：

- `solution.c`（AI 参考实现）
- `README.md`（含用户思路摘要）
- `meta.yaml`
- `review.md`

`review.md` 包含 `status`、`total_score`、评分细项和改进建议。

并自动重建：

- `index/by-module.md`
- `index/by-c-topic.md`

## 已完成基础题目（原有）

### 1. 删除最小值元素 (delete_min_element.c)
**题目**: 从顺序表中删除具有最小值的元素，空出的位置由最后一个元素填补。

**算法要点**:
- 时间复杂度: O(n)
- 空间复杂度: O(1)
- 遍历一次找到最小值位置，用最后一个元素填补

### 2. 逆置顺序表 (reverse_list.c)
**题目**: 设计一个高效算法，将顺序表 L 的所有元素逆置，要求空间复杂度为 O(1)。

**算法要点**:
- 时间复杂度: O(n)
- 空间复杂度: O(1)
- 双指针法：左右指针向中间移动并交换元素

### 3. 删除所有值为 x 的元素 (delete_all_value.c)
**题目**: 编写时间复杂度 O(n)、空间复杂度 O(1) 的算法，删除顺序表中所有值为 x 的元素。

**算法要点**:
- 时间复杂度: O(n)
- 空间复杂度: O(1)
- 计数法：记录保留元素个数，原地覆盖

### 4. 删除范围内的元素 (delete_range.c)
**题目**: 从顺序表中删除值在给定范围 [s, t] 内（包含 s 和 t）的所有元素。若参数不合理或顺序表为空，则显示错误信息并退出。

**算法要点**:
- 时间复杂度: O(n)
- 空间复杂度: O(1)
- 参数合法性检查 + 计数法筛选

## 本地运行

### 1) 安装前端依赖并构建页面

```bash
npm --prefix apps/web install
npm --prefix apps/web run build
```

### 2) 启动 API（含 Web 页面）

```bash
PYTHONPATH=. uv run --with fastapi --with pydantic --with uvicorn --with httpx \
  uvicorn apps.api.main:app --reload
```

打开 `http://127.0.0.1:8000/` 即可使用 Web 页面。

可选：启用真实 AI 评审（未设置时自动使用本地规则评审）

```bash
export OPENAI_API_KEY="<your-key>"
export AI_REVIEW_MODEL="gpt-4o-mini"
# 可选自定义兼容端点
# export OPENAI_API_BASE="https://api.openai.com/v1"
```

### 3) 运行后端与前端测试

```bash
bash scripts/check.sh
```

### 4) 本地前端环境变量

可复制 `apps/web/.env.example` 为 `apps/web/.env.local`，并按需调整：

```bash
cp apps/web/.env.example apps/web/.env.local
```

`VITE_API_BASE_URL` 默认值为 `http://127.0.0.1:8000`。

### 5) 构建并验证沙箱镜像

```bash
bash scripts/sandbox-build.sh
bash scripts/sandbox-smoke.sh
```

默认运行时是 `runsc`。若本机尚未安装 gVisor，可临时回退：

```bash
SANDBOX_RUNTIME=runc bash scripts/sandbox-smoke.sh
```

### 6) 旧 CMake 代码编译（Exercise 目录）

### 使用 CMake

```bash
# 创建构建目录
mkdir build
cd build

# 配置项目
cmake ..

# 编译
cmake --build .

# 运行
./Fudan
```

### 直接编译单个文件

```bash
gcc -o exercise Exercise/delete_min_element.c
./exercise
```

## 代码规范

- **注释**: 使用清晰的注释说明算法逻辑
- **输出**: 使用英文输出信息和错误提示
- **命名**: 函数名使用小驼峰命名法
- **复杂度**: 每个算法都标注时间和空间复杂度

## 学习建议

1. 理解核心算法思想
2. 掌握时间和空间复杂度分析
3. 注意边界条件处理（空表、单元素等）
4. 熟练运用常用技巧（双指针、计数法等）
5. 通过练习建立解题模板

## 参考资料

- 《数据结构》严蔚敏版
- 经典算法教材
- 在线编程平台

## 许可证

本项目仅用于个人学习和练习。

## 部署前端到 GitHub Pages

1. 在仓库 `Settings -> Pages` 中启用 GitHub Pages（来源使用 `gh-pages` 分支）。
2. 在仓库 `Settings -> Secrets and variables -> Actions -> Variables` 中新增 `VITE_API_BASE_URL`。
3. 推送 `dev` 分支触发 `.github/workflows/deploy-web.yml`。
4. CI 通过后会自动发布 `apps/web/dist` 到 `gh-pages` 分支。
5. 本地开发可复制 `apps/web/.env.example` 为 `apps/web/.env.local` 并按需修改。
