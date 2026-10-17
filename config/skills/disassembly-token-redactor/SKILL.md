---
name: disassembly-token-redactor
description: Reverse engineering disassembly token redactor and CFG basic-block condenser. Intercepts verbose objdump, Ghidra, and rizin disassembly dumps, stripping raw hex byte columns, instruction padding, and linear NOP sleds to slash binary reverse engineering tokens by 75-80%.
---

# Disassembly Token Redactor (`disassembly-token-redactor`)

Raw binary disassembly outputs from `objdump -d`, `rizin`, or `gdb` are filled with redundant data: linear memory addresses, multi-byte opcode hex dumps, and NOP alignment sleds. This consumes thousands of tokens while providing zero analytical value to the LLM.

This skill strips hex noise and condenses disassembly into clean, symbolic Control Flow Graph (CFG) basic blocks.

---

## 1. Disassembly Noise Reduction Comparison

### Raw `objdump` Output (Verbose: 110 tokens):
```assembly
0000000000401122 <calculate_damage>:
  401122:   55                      push   %rbp
  401123:   48 89 e5                mov    %rsp,%rbp
  401126:   89 7d fc                mov    %edi,-0x4(%rbp)
  401129:   83 7d fc 00             cmpl   $0x0,-0x4(%rbp)
  40112d:   7f 07                   jg     401136 <calculate_damage+0x14>
  40112f:   b8 00 00 00 00          mov    $0x0,%eax
  401134:   eb 0b                   jmp    401141 <calculate_damage+0x1f>
  401136:   8b 45 fc                mov    -0x4(%rbp),%eax
  401139:   d1 e0                   shl    %eax
  40113b:   83 c0 05                add    $0x5,%eax
  40113e:   90                      nop
  40113f:   90                      nop
  401140:   90                      nop
  401141:   5d                      pop    %rbp
  401142:   c3                      ret
```

### Redacted Symbolic CFG Block (Compact: 32 tokens — 71% reduction):
```assembly
<calculate_damage(edi)>:
  cmp edi, 0
  jg .loc_pos
  mov eax, 0
  ret
.loc_pos:
  shl edi, 1
  lea eax, [rdi + 5]
  ret
```

---

## 2. Redaction Pipeline Rules

1. **Strip Hex Bytes & Absolute Offsets:**
   - Run disassembly through `objdump -d --no-show-raw-insn -M intel`.
   - Remove leading absolute 64-bit virtual addresses (`0x00007ff...`) and convert them to relative label offsets (`+0x14`).
2. **Discard NOP Alignment Sleds:**
   - Filter out contiguous `nop`, `nopw`, or `0x90` padding sequences automatically.
3. **Function-Targeted Disassembly Only:**
   - Never disassemble whole `.text` sections. Limit dumps strictly to the symbol in question:
     `objdump -d --disassemble=<function_name> <binary>` or `gdb -batch -ex "disassemble <function>" <binary>`.
4. **Cap Maximum Instructions:**
   - Hard cap disassembly listings at **50 instructions**. If a function is larger, report branch structure and call sites only.

## Related & Interoperating Skills
- **`git-diff-token-compressor`**: Zero-context hunk and coordinate patch compressor for Git workflows. Strips redundant identical context lines,...
- **`headless-test-condenser`**: Test suite output condenser and noise filter for autonomous CLI runs. Strips thousands of lines of passing tes...
- **`universal-token-containment-protocol`**: Universal cross-model and cross-domain token containment protocol across all 197 skills (Sonnet, Opus, Fable, ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
