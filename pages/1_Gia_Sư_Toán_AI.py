def tron_dap_an(dung, sai_list):
    ds = sai_list + [dung]
    random.shuffle(ds)
    return ds
def tao_de_toan(lop, bai_hoc):
    de_latex = ""
    question_type = "mcq"
    dap_an = ""
    options = []
    goi_y_text = ""
    goi_y_latex = ""

    bai = bai_hoc.lower()

    # ================= LỚP 6 =================
    if "lớp 6" in lop.lower():

        # --- BÀI 1. TẬP HỢP ---
        if "bài 1" in bai or "tập hợp" in bai:

            if random.choice([0, 1]) == 0:
                tap = sorted(random.sample(range(1, 10), 5))
                dung = random.choice(tap)
                sai = random.choice([x for x in range(1, 12) if x not in tap])

                dap_an = f"{dung} ∈ {{{';'.join(map(str, tap))}}}"
                options = tron_dap_an(dap_an, [
                    f"{sai} ∈ {{{';'.join(map(str, tap))}}}",
                    f"{dung} ∉ {{{';'.join(map(str, tap))}}}",
                    f"{tap[0]} ⊂ {tap[1]}"
                ])

                de_latex = "Cách viết nào đúng?"
                goi_y_text = f"{dung} thuộc tập hợp đã cho."

            else:
                n = random.randint(3, 7)
                dap_an = "{" + ";".join(map(str, range(0, n))) + "}"
                options = tron_dap_an(dap_an, [
                    "{" + ";".join(map(str, range(1, n))) + "}",
                    "{" + ";".join(map(str, range(0, n+1))) + "}",
                    "{" + ";".join(map(str, range(1, n+1))) + "}"
                ])
                de_latex = f"Tập hợp A = {{x | x là số tự nhiên nhỏ hơn {n}}} là:"
                goi_y_text = f"Số tự nhiên nhỏ hơn {n} gồm từ 0 đến {n-1}."

        # --- BÀI 6. LŨY THỪA ---
        elif "bài 6" in bai or "lũy thừa" in bai:
            a = random.randint(2, 5)
            n = random.randint(2, 3)
            dap_an = str(a ** n)
            options = tron_dap_an(dap_an, [
                str(a * n),
                str(a + n),
                str(a ** (n + 1))
            ])
            de_latex = f"Tính giá trị: ${a}^{n}$"
            goi_y_text = "Lũy thừa là nhân số đó với chính nó nhiều lần."
            goi_y_latex = f"{a}^{n} = " + "×".join([str(a)] * n)

    # ================= LỚP 7 =================
    elif "lớp 7" in lop.lower():
        a = random.randint(2, 9)
        dap_an = str(a * a)
        options = tron_dap_an(dap_an, [str(a), str(-a), str(a*2)])
        de_latex = f"Tính: $(-{a})^2$"
        goi_y_text = "Bình phương của số âm là số dương."
        goi_y_latex = f"(-{a})^2 = {a}^2"

    # ================= LỚP 8 =================
    elif "lớp 8" in lop.lower():
        a = random.randint(2, 5)
        dap_an = f"{a}x"
        options = tron_dap_an(dap_an, [f"-{a}x", "x²", f"{a}"])
        de_latex = f"Rút gọn: $x(x+{a}) - x^2$"
        goi_y_text = "Khai triển rồi thu gọn."
        goi_y_latex = f"x^2 + {a}x - x^2 = {a}x"

    # ================= LỚP 9 =================
    elif "lớp 9" in lop.lower():
        a = random.randint(2, 9)
        dap_an = f"x ≥ {a}"
        options = tron_dap_an(dap_an, [
            f"x > {a}", f"x ≤ {a}", f"x < {a}"
        ])
        de_latex = f"Điều kiện xác định của $\\sqrt{{x-{a}}}$ là:"
        goi_y_text = "Biểu thức trong căn bậc hai phải không âm."
        goi_y_latex = f"x - {a} ≥ 0 ⇔ x ≥ {a}"

    # ================= FALLBACK =================
    else:
        a, b = random.randint(1, 20), random.randint(1, 20)
        dap_an = str(a + b)
        options = tron_dap_an(dap_an, [
            str(a+b+1), str(a+b-1), str(a+b+2)
        ])
        de_latex = f"Tính: {a} + {b}"
        goi_y_text = "Cộng hai số tự nhiên."

    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex
