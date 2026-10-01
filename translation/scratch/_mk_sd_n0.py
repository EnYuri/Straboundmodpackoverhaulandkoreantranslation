# -*- coding: utf-8 -*-
import sys, io, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Real firearm/military designations stay in Latin script per convention.
KEEP = """AEK-971 AEK-973 AK-101 AK-102 AK-103 AK-104 AK-105 AK-106 AK-107 AK-108
AK-109 AK-12 AK-12/410 AK-15 AK-19 AK-200 AK-201 AK-202 AK-203 AK-204 AK-205
AK-24 AK-26 AK-28 AK-308 AK-337 AK-351 AK-50L AK-74 AK-74M AK-9 AK-Alfa AK-X
AKE-40 AKS-74 AKS-74M AKS-74U AKS-74UM AKV-521 AKX-1 AKX-2 AN-94 AR-10 AR-15
AR-18 AR-57 AWGL-3 BAR-15 BVAR-80 BZR-64 CS/LR28 EM-94 FG-8 FTAC-12 GSW-AR
GSW-DMR KS-23 LR-300 LRGL-25 M-1000 MAC-10 MGL-140 MP-40 MP5-SD MTs-255 NL-545
OSR-DEMOL OSR-M1 OSR-M2 PPK-20 PPSH-41 PPsH-2600 PPsH-41 PRG-41 QBZ-192 R-103
R-105 R-113 R-120 R-91 RK-6 RPG-7 RPK-16 RPK-74 RPK-74M RSM-48 RSh-9 SAR-2
SAR-3 SCAR-H SCAR-L SFC-35 SL-8 SOVA-545N SOVA-762 SOVA-GB SPAS-12 SR-3M
SVT-40 Saiga-12 Saiga-3006 Saiga-308 Saiga-762 StG-940 TKB-022PM TR-3 TR-4
Tec-9 UMP-45 USCM-4 USCMStar VPO-209 Vepr-12 Vepr-3006 Vepr-308 Vepr-762 XME-8""".split()

w = csv.writer(open("data/_uncov_ko_sd_n0.tsv", "w", encoding="utf-8", newline=""), delimiter="\t")
w.writerow(["en", "ko"])
for e in KEEP:
    w.writerow([e, e])
print("sd_n0", len(KEEP))
