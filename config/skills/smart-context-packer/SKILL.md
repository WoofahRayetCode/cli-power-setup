---
name: smart-context-packer
description: Compresses multi-file codebases into interface-only AST skeletons (stripping function bodies, comments, and blank lines), reducing context consumption by 85-90%.
---

# Smart Context Packer & AST Codebase Skeletons

This skill creates high-density, interface-only code skeletons of large repositories or subsystems, allowing the AI to understand architectural connections across dozens of files in <4,000 tokens instead of 50,000+ tokens.

---

## 📐 Why Interface-Only Packing Works

When planning a refactor or understanding an unfamiliar subsystem, the AI does **not** need the internal loop implementations of 20 different files. It only needs:
1. Class and struct names
2. Exported methods and signatures
3. Field types and inheritance
4. Public constants and enums

---

## 🛠️ 1. Skeleton Extraction Patterns

Extract lightweight headers from source files:

### Python Skeleton (Using stdlib `ast` or regex):
```bash
python3 - << 'EOF'
import ast, sys

class SkeletonVisitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        print(f"class {node.name}:")
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                args = [a.arg for a in item.args.args]
                print(f"    def {item.name}({', '.join(args)}): ...")
    def visit_FunctionDef(self, node):
        args = [a.arg for a in node.args.args]
        print(f"def {node.name}({', '.join(args)}): ...")

with open("my_large_module.py") as f:
    tree = ast.parse(f.read())
SkeletonVisitor().visit(tree)
EOF
```

### C++ Header Skeletons:
Strip inline implementations, keeping declarations:
```bash
grep -E '^(class|struct|virtual|void|int|bool|std::)' include/engine.h | grep -v '{'
```

---

## 📉 Token Savings Impact
* Full source read of 10 files (5,000 lines): **~40,000 input tokens**.
* Interface skeleton of 10 files (400 lines): **~3,200 input tokens** (92% reduction).

---

## 🔄 Interoperability & Handoffs

* **Handoff to `semantic-codebase-indexing`:** Uses symbol index tags to identify which files to skeletonize.
* **Handoff to `writing-plans`:** Feeds interface skeletons into implementation plans without blowing the context window.
