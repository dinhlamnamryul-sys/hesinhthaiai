# ===== BÀI 1. TẬP HỢP =====
elif bai == "Bài 1. Tập hợp":

    dang = random.choice([1, 2])

    # ---- DẠNG 1: PHẦN TỬ THUỘC TẬP HỢP ----
    if dang == 1:
        tap = sorted(random.sample(range(1, 10), 5))
        x_dung = random.choice(tap)
        x_sai = random.choice([x for x in range(1, 12) if x not in tap])

        cau_hoi = (
            f"Cho tập hợp $A=\\{{{';'.join(map(str, tap))}\\}}$. "
            f"Cách viết nào đúng?"
        )

        dap_an = f"${x_dung}\\in A$"

        options = [
            f"${x_dung}\\in A$",
            f"${x_sai}\\in A$",
            f"${x_dung}\\notin A$",
            f"${tap[0]}\\subset{tap[1]}$"
        ]

        goi_y_viet = (
            "Dấu $\\in$ có nghĩa là 'thuộc'. "
            "Một số thuộc tập hợp nếu nó nằm trong danh sách các phần tử của tập hợp đó."
        )

        goi_y_latex = f"{x_dung}\\in\\{{{';'.join(map(str, tap))}\\}}"

    # ---- DẠNG 2: VIẾT TẬP HỢP ----
    else:
        n = random.randint(4, 7)
        cau_hoi = (
            f"Tập hợp $A$ gồm các số tự nhiên nhỏ hơn ${n}$ là:"
        )

        dap_an = "$A=\\{0;1;2;3\\}$" if n == 4 else f"$A=\\{{0;1;2;\\ldots;{n-1}\\}}$"

        options = [
            dap_an,
            f"$A=\\{{1;2;3;\\ldots;{n}\\}}$",
            f"$A=\\{{1;2;3;\\ldots;{n-1}\\}}$",
            f"$A=\\{{0;1;2;\\ldots;{n}\\}}$"
        ]

        goi_y_viet = (
            "Số tự nhiên bao gồm cả số 0. "
            "Cụm từ 'nhỏ hơn' nghĩa là không lấy số đó."
        )

        goi_y_latex = f"A=\\{{0;1;2;\\ldots;{n-1}\\}}"

    random.shuffle(options)

    return cau_hoi, dap_an, options, goi_y_viet, goi_y_latex
