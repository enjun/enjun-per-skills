#!/usr/bin/env python3
"""
快速验证脚本：检查 independent-scientific-research 技能的基本结构
"""

import os
import sys
import json
from pathlib import Path

# 技能根目录
SKILL_ROOT = Path(__file__).parent.parent

def check_file_exists(path, description):
    """检查文件是否存在"""
    if path.exists():
        print(f"[OK] {description}: {path.name}")
        return True
    else:
        print(f"[FAIL] {description}: {path} does not exist")
        return False

def check_json_structure(path, required_keys, description):
    """检查JSON文件结构"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        missing = [k for k in required_keys if k not in data]
        if missing:
            print(f"[FAIL] {description}: Missing keys {missing}")
            return False
        print(f"[OK] {description}: Structure correct")
        return True
    except Exception as e:
        print(f"[FAIL] {description}: {e}")
        return False

def check_markdown_structure(path, required_sections, description):
    """检查Markdown文件结构"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        missing = []
        for section in required_sections:
            if section not in content:
                missing.append(section)
        if missing:
            print(f"[FAIL] {description}: Missing sections {missing}")
            return False
        print(f"[OK] {description}: Contains all required sections")
        return True
    except Exception as e:
        print(f"[FAIL] {description}: {e}")
        return False

def main():
    print("=" * 60)
    print("验证 independent-scientific-research 技能")
    print("=" * 60)

    checks = []

    # 1. 检查主文件
    print("\n1. 主文件检查")
    checks.append(check_file_exists(
        SKILL_ROOT / "SKILL.md",
        "主技能文档"
    ))

    # 2. 检查 references 目录
    print("\n2. 参考文档检查")
    refs_dir = SKILL_ROOT / "references"

    ref_files = [
        ("agent_prompts.md", "Agent prompt模板"),
        ("proposer_brainstorming.md", "Proposer头脑风暴方法"),
        ("experiment_guide.md", "实验设计指南"),
        ("ris-code-integration.md", "RIS仿真模块"),
    ]

    for filename, desc in ref_files:
        checks.append(check_file_exists(refs_dir / filename, desc))

    # 3. 检查 SKILL.md 结构
    print("\n3. SKILL.md 结构检查")
    required_sections = [
        "## Stage 1: Problem Analysis",
        "## Stage 2: Proposer",
        "## Stage 3: Parallel Debate",
        "## Stage 4: Evaluator",
        "## Stage 5: Final Output",
    ]
    checks.append(check_markdown_structure(
        SKILL_ROOT / "SKILL.md",
        required_sections,
        "SKILL.md"
    ))

    # 4. 检查 agent_prompts.md 结构
    print("\n4. Agent Prompts 结构检查")
    agent_prompts = refs_dir / "agent_prompts.md"
    required_agent_sections = [
        "## Stage 2: Proposer Agent",
        "## Stage 3: Supporter Agent",
        "## Stage 3: Critic Agent",
        "## Stage 4: Evaluator Agent",
    ]
    checks.append(check_markdown_structure(
        agent_prompts,
        required_agent_sections,
        "agent_prompts.md"
    ))

    # 5. 检查 proposer_brainstorming.md 结构
    print("\n5. 头脑风暴方法检查")
    brainstorming = refs_dir / "proposer_brainstorming.md"
    required_brainstorm_sections = [
        "### 第一阶段：发散探索",
        "### 第二阶段：建立联系",
        "### 第三阶段：批判性评估",
        "### 第四阶段：方案综合",
    ]
    checks.append(check_markdown_structure(
        brainstorming,
        required_brainstorm_sections,
        "proposer_brainstorming.md"
    ))

    # 6. 检查测试用例
    print("\n6. 测试用例检查")
    evals_file = SKILL_ROOT / "evals" / "evals.json"
    checks.append(check_json_structure(
        evals_file,
        ["skill_name", "evals"],
        "evals.json"
    ))

    # 7. 检查 assets 目录
    print("\n7. LaTeX 模板检查")
    assets_dir = SKILL_ROOT / "assets"
    template_files = [
        ("IEEEtran.cls", "IEEE文档类"),
        ("IEEEtran.bst", "IEEE参考文献样式"),
        ("main.tex", "LaTeX主模板"),
    ]
    for filename, desc in template_files:
        checks.append(check_file_exists(assets_dir / filename, desc))

    # 总结
    print("\n" + "=" * 60)
    passed = sum(checks)
    total = len(checks)
    print(f"Validation Result: {passed}/{total} passed")
    print("=" * 60)

    if passed == total:
        print("\n[OK] Skill structure is complete, ready for testing")
        return 0
    else:
        print(f"\n[FAIL] Skill structure incomplete, fix {total - passed} issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
