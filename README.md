# ISCE2 + MintPy SBAS-InSAR Skill

[![GitHub repository](https://img.shields.io/badge/GitHub-ISCE2--MintPy--SBASInSAR-181717?logo=github)](https://github.com/sinerdddddd/ISCE2-mintpy-SBASInSAR)
[![Skill](https://img.shields.io/badge/Codex-Skill-0B6E4F)](https://github.com/sinerdddddd/ISCE2-mintpy-SBASInSAR)

**简体中文** | [English](#english)

## 项目简介

`isce2-mintpy-sbas-insar` 是一个面向 Agent 的 InSAR 处理 skill，用于辅助完成基于 Sentinel-1 TOPS 数据的 ISCE2 + MintPy SBAS-InSAR 项目。它将环境检查、项目参数解析、ISCE2 干涉图栈处理、MintPy 时序反演、ERA5 对流层延迟校正、结果验证和 GeoTIFF 导出组织成可检查、可恢复的工作流。

本 skill 由**山东科技大学海洋学院张翼课题组**主持开发：

- **课题组负责人**：张翼，邮箱：[yizhang@sdust.edu.cn](mailto:yizhang@sdust.edu.cn)
- **研发**：罗赣，邮箱：[2889879473@qq.com](mailto:2889879473@qq.com)
- **测试参与**：王柏涵
- **版权归属**：山东科技大学海洋学院张翼课题组

> 本项目是科研处理辅助工具。实际处理结果取决于数据质量、软件版本、计算资源、参数设置和具体研究区，使用前请结合项目需求进行独立检查。

## 这个 skill 能做什么？

在用户提供项目路径、数据范围和运行环境后，Agent 可以使用本 skill：

- 检查 ISCE2、MintPy、HDF5、GDAL 等软件和 Python 模块是否可用；
- 梳理 Sentinel-1 SLC、轨道、DEM、辅助数据、AOI 和时间范围；
- 规划并执行 ISCE2 `stackSentinel.py` / `topsStack` 处理流程；
- 生成和分阶段执行本地或 SLURM 集群任务；
- 按检查点推进流程，避免在上游失败时盲目提交下游任务；
- 加载干涉图和几何数据到 MintPy，完成网络反演、时序、速度和相干性分析；
- 根据日期覆盖、时间和空间范围等条件执行或跳过 ERA5/PyAPS3 对流层校正；
- 导出适用于机器学习或 GIS 分析的 GeoTIFF/HDF5 产品；
- 对关键输出进行文件、数量、维度、元数据、CRS、NoData 和校验和检查；
- 根据日志和检查点定位错误，并从最小安全重启点恢复任务；
- 汇总运行配置、软件版本、处理日志、结果产品和质量控制证据。

## 工作流

本 skill 将项目状态组织为以下阶段：

```text
prepare
  -> stack_configured
  -> isce_completed
  -> mintpy_loaded
  -> inversion_completed
  -> troposphere_corrected
  -> exports_verified
```

每个阶段完成后，Agent 都应先检查相应的成功条件，再继续下一阶段。详细规则见：

- [工作流与断点续跑](references/workflow.md)
- [项目参数约定](references/parameters.md)
- [验证清单](references/validation.md)
- [故障排查](references/troubleshooting.md)
- [ERA5/PyAPS3 说明](references/era5.md)

## 安装与使用

### 1. 安装本 skill

建议在支持 Codex skill 的 Agent 中，将本仓库作为 skill 安装。安装完成后，skill 名称为：

```text
isce2-mintpy-sbas-insar
```

安装后可以使用以下调用方式：

```text
$isce2-mintpy-sbas-insar
```

### 2. 让 Agent 安装本 skill 的提示词

可以直接复制下面的提示词发送给 Agent：

```text
请从 GitHub 仓库 https://github.com/sinerdddddd/ISCE2-mintpy-SBASInSAR
安装名为 isce2-mintpy-sbas-insar 的 skill。

安装完成后请：
1. 检查 SKILL.md、agents/openai.yaml、references/ 和 scripts/ 是否安装完整；
2. 读取 SKILL.md，确认该 skill 可以用于 Sentinel-1 TOPS 的 ISCE2 + MintPy SBAS-InSAR 工作流；
3. 告诉我安装结果、skill 的调用名称，以及如何用它执行项目预检。
不要修改我的 InSAR 数据、环境或已有项目文件。
```

如果 Agent 已经安装完成，也可以直接使用：

```text
请使用 $isce2-mintpy-sbas-insar。
先读取 skill 的 SKILL.md 和 references/workflow.md，
然后检查项目目录并运行只读预检。
在确认环境、输入数据和项目参数后，再给出分阶段执行计划。
不要猜测路径、日期、AOI、资源配置或软件版本。
```

### 3. 推荐的首次使用提示词

```text
请使用 $isce2-mintpy-sbas-insar 处理我的 Sentinel-1 TOPS SBAS-InSAR 项目。

项目目录：/path/to/project
SLC 目录：/path/to/project/SLC
轨道目录：/path/to/project/orbits
DEM：/path/to/project/DEM/dem.wgs84
研究区 AOI：请从我的配置文件或数据范围中读取
时间范围：请从输入数据中核对
运行环境：Linux + SLURM / 本地 Linux（二选一，并以实际环境为准）

请先执行只读预检，不要提交作业，不要删除或覆盖任何文件。
请在预检后报告：
1. 缺失的软件、模块、输入文件或目录；
2. 需要我确认的参数；
3. 分阶段执行计划；
4. 每一阶段的成功判据和失败后的安全恢复方式。
```

### 4. 手动执行只读检查

在项目环境已经配置好的情况下，可以直接运行：

```bash
python scripts/preflight_check.py /path/to/project
```

完成 ISCE2 和 MintPy 处理后，可以运行：

```bash
python scripts/validate_outputs.py /path/to/project
```

预检脚本会检查项目目录、常用可执行程序和关键 Python 模块；输出验证脚本会检查常见干涉图产品、MintPy HDF5 文件、时序结果和 GeoTIFF 目录。脚本只负责检查，不会替用户删除数据或重建项目。

## 目录结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── era5.md
│   ├── parameters.md
│   ├── troubleshooting.md
│   ├── validation.md
│   ├── workflow.md
│   └── ISCE2_MintPy_SBAS-InSAR_处理操作手册_ERA5解决办法补充版.docx
└── scripts/
    ├── preflight_check.py
    └── validate_outputs.py
```

## 结果与质量控制

在项目条件允许的情况下，Agent 应汇报以下内容：

- ISCE2 配置文件、运行脚本和日志；
- `inputs/ifgramStack.h5` 与 `inputs/geometryRadar.h5`；
- MintPy 速度、时序、相干性和地理编码结果；
- ERA5 校正输入、覆盖日期、校正后产品及版本信息；
- ML/GIS 使用的 GeoTIFF 或 HDF5 输出；
- `pairs.csv`、归档文件和校验和清单；
- 未完成的检查、使用的假设以及仍需人工确认的事项。

## 反馈、测试与协作

欢迎从事 InSAR、遥感、地学和形变监测研究的同行试用本 skill，并通过 GitHub Issues 提交可复现的问题、日志片段、运行环境和改进建议。你的反馈将帮助我们完善不同数据集、软件版本和计算平台下的兼容性。

如果这个 skill 对你的研究或数据处理有所帮助，欢迎在 GitHub 仓库中点亮 Star，并将项目分享给可能需要的同行。

## 版权与致谢

本 skill 的版权归**山东科技大学海洋学院张翼课题组**所有。项目中涉及的 ISCE2、MintPy、PyAPS3、GDAL 及其他软件和数据，应遵循各自的许可证、使用条款和数据政策。

如需用于论文、报告或二次开发，建议在适当位置说明本 skill 的项目地址，并同时引用实际使用的软件、数据源和算法。

---

<a id="english"></a>

# English

## Overview

`isce2-mintpy-sbas-insar` is an Agent-oriented InSAR processing skill for Sentinel-1 TOPS SBAS-InSAR projects based on ISCE2 and MintPy. It organizes environment checks, project configuration, ISCE2 interferogram-stack processing, MintPy time-series inversion, optional ERA5 tropospheric correction, output validation, and GeoTIFF export into a check-pointed and restartable workflow.

This skill is led and developed by the **Zhang Yi Research Group, College of Oceanography, Shandong University of Science and Technology**:

- **Group leader**: Yi Zhang, [yizhang@sdust.edu.cn](mailto:yizhang@sdust.edu.cn)
- **Developer**: Gan Luo, [2889879473@qq.com](mailto:2889879473@qq.com)
- **Testing contributor**: Baihan Wang
- **Copyright**: Zhang Yi Research Group, College of Oceanography, Shandong University of Science and Technology

> This project is a research-processing assistant. Results depend on data quality, software versions, computational resources, processing parameters, and the study area. Independent verification is recommended for every scientific application.

## Capabilities

After the user provides the project paths, data scope, and execution environment, the Agent can use this skill to:

- check ISCE2, MintPy, HDF5, GDAL, and required Python modules;
- organize Sentinel-1 SLC, orbit, DEM, auxiliary data, AOI, and date-range inputs;
- plan and run the ISCE2 `stackSentinel.py` / `topsStack` workflow;
- generate and execute staged local or SLURM jobs;
- enforce checkpoint-based execution so downstream jobs are not submitted after an upstream failure;
- load interferogram and geometry products into MintPy for network inversion, time series, velocity, and coherence analysis;
- apply or intentionally skip ERA5/PyAPS3 tropospheric correction after date and coverage checks;
- export GeoTIFF/HDF5 products for machine-learning or GIS workflows;
- validate files, product counts, dimensions, metadata, CRS, NoData values, and checksums;
- diagnose failures from logs and checkpoints and resume from the smallest safe restart point;
- report configurations, software versions, logs, products, and quality-control evidence.

## Workflow

The skill models the project as the following sequence:

```text
prepare
  -> stack_configured
  -> isce_completed
  -> mintpy_loaded
  -> inversion_completed
  -> troposphere_corrected
  -> exports_verified
```

Each stage should be validated before the next stage is started. See:

- [Workflow and restart rules](references/workflow.md)
- [Project configuration contract](references/parameters.md)
- [Validation checklist](references/validation.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [ERA5/PyAPS3 guidance](references/era5.md)

## Installation and Usage

### 1. Install the skill

Install this repository as a skill in an Agent that supports Codex skills. The skill name is:

```text
isce2-mintpy-sbas-insar
```

After installation, invoke it with:

```text
$isce2-mintpy-sbas-insar
```

### 2. Prompt for installing the skill

The following prompt can be copied directly:

```text
Please install the skill named isce2-mintpy-sbas-insar from the GitHub repository:
https://github.com/sinerdddddd/ISCE2-mintpy-SBASInSAR

After installation:
1. Check that SKILL.md, agents/openai.yaml, references/, and scripts/ are installed;
2. Read SKILL.md and confirm that the skill supports Sentinel-1 TOPS ISCE2 + MintPy SBAS-InSAR workflows;
3. Report the installation result, the invocation name, and how to run a read-only project preflight.
Do not modify my InSAR data, software environment, or existing project files.
```

If the skill is already installed, use:

```text
Please use $isce2-mintpy-sbas-insar.
First read SKILL.md and references/workflow.md, then run a read-only preflight
against my project directory. After the environment, inputs, and project
parameters are confirmed, provide a staged execution plan. Do not guess paths,
dates, AOI, resource settings, or software versions.
```

### 3. Recommended first-run prompt

```text
Please use $isce2-mintpy-sbas-insar to process my Sentinel-1 TOPS SBAS-InSAR project.

Project directory: /path/to/project
SLC directory: /path/to/project/SLC
Orbit directory: /path/to/project/orbits
DEM: /path/to/project/DEM/dem.wgs84
AOI: read and verify it from my configuration or input data
Date range: inspect and verify it from the input data
Execution environment: Linux + SLURM / local Linux (use the actual environment)

Run a read-only preflight first. Do not submit jobs and do not delete or
overwrite any files. After the preflight, report:
1. missing software, modules, inputs, or directories;
2. parameters that require confirmation;
3. a staged execution plan;
4. the success criteria and safe recovery method for each stage.
```

### 4. Run the read-only checks manually

With the project environment configured, run:

```bash
python scripts/preflight_check.py /path/to/project
```

After ISCE2 and MintPy processing, run:

```bash
python scripts/validate_outputs.py /path/to/project
```

The preflight script checks project directories, executables, and Python modules. The output validator checks common interferogram products, MintPy HDF5 files, time-series products, and the GeoTIFF directory. These scripts are read-only: they do not delete data or rebuild the project.

## Feedback and Collaboration

Researchers working with InSAR, remote sensing, geoscience, and deformation monitoring are welcome to test this skill. Please use GitHub Issues to report reproducible problems and include the relevant logs, software versions, input characteristics, and execution platform when possible.

If this skill is useful for your research or processing workflow, please consider giving the repository a Star and sharing it with colleagues who may benefit from it.

## Copyright and Acknowledgements

Copyright belongs to the **Zhang Yi Research Group, College of Oceanography, Shandong University of Science and Technology**. ISCE2, MintPy, PyAPS3, GDAL, and other third-party software and data remain subject to their respective licenses, terms of use, and data policies.

For use in papers, reports, or derivative work, please acknowledge this skill where appropriate and cite the software, data sources, and algorithms used in the actual analysis.

