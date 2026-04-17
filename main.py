# -*- coding: utf-8 -*-
"""
Bài toán quỹ đạo chất điểm trong mặt phẳng Oxy:
    x(t) = x0 * cos(5t)
    y(t) = y0 * cos(5t + phi)

Mục tiêu:
- Nhập x0, y0, phi từ bàn phím.
- Dùng sympy để biểu diễn symbolic và suy ra phương trình quỹ đạo không tham số.
- Dùng matplotlib để vẽ quỹ đạo tham số.
"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


def classify_orbit(x0_val: float, y0_val: float, phi_val: float, eps: float = 1e-10) -> str:
    """Phân loại dạng quỹ đạo theo các trường hợp của phi, x0, y0."""
    s = np.sin(phi_val)
    c = np.cos(phi_val)

    # Trường hợp phi = k*pi => sin(phi)=0, hai dao động cùng/ ngược pha -> đường thẳng
    if abs(s) < eps:
        if abs(x0_val) < eps and abs(y0_val) < eps:
            return "Suy biến tại gốc O (chất điểm đứng yên tại (0,0))."
        if c > 0:
            return "Đường thẳng: y = (y0/x0) * x (khi x0 != 0)."
        return "Đường thẳng: y = -(y0/x0) * x (khi x0 != 0)."

    # Trường hợp tổng quát: Lissajous tỉ số tần số 1:1, thường là elip
    return "Đường cong Lissajous tỉ số 1:1 (dạng elip tổng quát; có thể suy biến tùy tham số)."


def symbolic_derivation(x0_val: float, y0_val: float, phi_val: float):
    """
    Dùng sympy + biến đổi thủ công để loại t.

    Vì hai phương trình chứa cos(5t) và cos(5t+phi), ta đặt u = 5t:
        x = x0*cos(u)
        y = y0*cos(u+phi) = y0*(cos(u)cos(phi) - sin(u)sin(phi))

    Nếu x0*y0 != 0:
        X = x/x0 = cos(u)
        Y = y/y0 = cos(u+phi)
        => Y = X*cos(phi) - sin(u)*sin(phi)
        => (Y - X*cos(phi))^2 = sin^2(phi)*(1 - X^2)
        => X^2 - 2*cos(phi)*X*Y + Y^2 = sin^2(phi)

    Suy ra theo x,y:
        x^2/x0^2 - 2*cos(phi)*x*y/(x0*y0) + y^2/y0^2 = sin^2(phi)
    """
    # 1) Khai báo biến symbolic
    t = sp.symbols("t", real=True)
    x0, y0, phi = sp.symbols("x0 y0 phi", real=True)
    x, y = sp.symbols("x y", real=True)

    # 2) Biểu diễn x(t), y(t)
    x_t = x0 * sp.cos(5 * t)
    y_t = y0 * sp.cos(5 * t + phi)

    # 3) Phương trình quỹ đạo không tham số (dạng tổng quát khi x0*y0 != 0)
    orbit_eq_xy = sp.Eq(
        x**2 / x0**2 - 2 * sp.cos(phi) * x * y / (x0 * y0) + y**2 / y0**2,
        sp.sin(phi) ** 2,
    )

    orbit_eq_numeric = sp.simplify(
        orbit_eq_xy.subs({x0: x0_val, y0: y0_val, phi: phi_val})
    )

    return t, x_t, y_t, orbit_eq_xy, orbit_eq_numeric


def plot_orbit_interactive(x0_val: float, y0_val: float, phi_val: float):
    """Vẽ đồ thị đẹp + cho phép chỉnh x0, y0, phi trực tiếp bằng slider."""
    # Dải thời gian cho 4 chu kỳ
    T = 2 * np.pi / 5
    t_vals = np.linspace(0, 4 * T, 1400)

    # Tạo figure với theme sáng, dễ quan sát
    fig, ax = plt.subplots(figsize=(9, 8))
    fig.patch.set_facecolor("#f7f7f7")
    ax.set_facecolor("#fcfcfc")
    plt.subplots_adjust(left=0.12, right=0.95, bottom=0.28, top=0.90)

    def compute_xy(a: float, b: float, p: float):
        x = a * np.cos(5 * t_vals)
        y = b * np.cos(5 * t_vals + p)
        return x, y

    x_vals, y_vals = compute_xy(x0_val, y0_val, phi_val)

    # Đường quỹ đạo + điểm bắt đầu
    (line,) = ax.plot(x_vals, y_vals, color="#005bbb", linewidth=2.5, label="Quỹ đạo")
    start_point = ax.scatter([x_vals[0]], [y_vals[0]], color="#d7263d", s=45, zorder=5, label="Điểm bắt đầu")

    # Trang trí trục
    ax.axhline(0, color="#222222", linewidth=1.0)
    ax.axvline(0, color="#222222", linewidth=1.0)
    ax.grid(True, linestyle="--", linewidth=0.7, alpha=0.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    title = ax.set_title("Quỹ đạo tương tác: x=x0cos(5t), y=y0cos(5t+phi)", fontsize=13, weight="bold")

    # Đưa legend ra ngoài vùng vẽ để không che đường quỹ đạo
    legend = ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0, frameon=True)
    legend.get_frame().set_alpha(0.9)

    # Giới hạn ban đầu
    lim = max(1.2, abs(x0_val), abs(y0_val)) + 0.5
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    # Tạo thanh trượt
    ax_x0 = plt.axes([0.16, 0.18, 0.70, 0.03], facecolor="#ececec")
    ax_y0 = plt.axes([0.16, 0.13, 0.70, 0.03], facecolor="#ececec")
    ax_phi = plt.axes([0.16, 0.08, 0.70, 0.03], facecolor="#ececec")

    slider_x0 = Slider(ax_x0, "x0", -5.0, 5.0, valinit=x0_val, valstep=0.05)
    slider_y0 = Slider(ax_y0, "y0", -5.0, 5.0, valinit=y0_val, valstep=0.05)
    slider_phi = Slider(ax_phi, "phi", -2 * np.pi, 2 * np.pi, valinit=phi_val, valstep=0.01)

    # Nút reset
    ax_reset = plt.axes([0.02, 0.08, 0.10, 0.06])
    btn_reset = Button(ax_reset, "Reset", color="#d9d9d9", hovercolor="#c7c7c7")

    # Nhãn thông tin nhanh về dạng quỹ đạo
    # Đưa nhãn thông tin xuống dưới figure để tránh che đồ thị
    info_text = fig.text(
        0.12,
        0.015,
        classify_orbit(x0_val, y0_val, phi_val),
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.9, edgecolor="#bbbbbb"),
    )

    def update(_):
        a = slider_x0.val
        b = slider_y0.val
        p = slider_phi.val

        x_new, y_new = compute_xy(a, b, p)
        line.set_data(x_new, y_new)

        # Cập nhật điểm bắt đầu
        start_point.set_offsets(np.array([[x_new[0], y_new[0]]]))

        # Cập nhật giới hạn trục theo biên độ mới
        lim_new = max(1.2, abs(a), abs(b)) + 0.5
        ax.set_xlim(-lim_new, lim_new)
        ax.set_ylim(-lim_new, lim_new)

        info_text.set_text(classify_orbit(a, b, p))
        title.set_text(f"Quỹ đạo tương tác: x0={a:.2f}, y0={b:.2f}, phi={p:.2f} rad")
        fig.canvas.draw_idle()

    slider_x0.on_changed(update)
    slider_y0.on_changed(update)
    slider_phi.on_changed(update)

    def reset(_):
        slider_x0.reset()
        slider_y0.reset()
        slider_phi.reset()

    btn_reset.on_clicked(reset)
    plt.show()


def main():
    print("=== BÀI TOÁN QUỸ ĐẠO CHẤT ĐIỂM ===")
    print("x(t) = x0 * cos(5t)")
    print("y(t) = y0 * cos(5t + phi)")
    print("Lưu ý: phi nhập theo radian.\n")

    # 1) Nhập dữ liệu ban đầu
    x0_val = float(input("Nhập x0: "))
    y0_val = float(input("Nhập y0: "))
    phi_val = float(input("Nhập phi (radian): "))

    # 2) Xử lý symbolic và loại tham số t
    t, x_t, y_t, orbit_eq_xy, orbit_eq_numeric = symbolic_derivation(x0_val, y0_val, phi_val)

    print("\n--- KẾT QUẢ SYMBOLIC ---")
    print("Biến symbolic t =", t)
    print("x(t) =", x_t)
    print("y(t) =", y_t)

    print("\nPhương trình quỹ đạo tổng quát theo x, y:")
    sp.pprint(sp.simplify(orbit_eq_xy), use_unicode=True)

    print("\nPhương trình quỹ đạo sau khi thế số x0, y0, phi:")
    sp.pprint(orbit_eq_numeric, use_unicode=True)

    # 3) Kết luận hình học
    print("\n--- KẾT LUẬN DẠNG QUỸ ĐẠO ---")
    conclusion = classify_orbit(x0_val, y0_val, phi_val)
    print(conclusion)

    # 4) Vẽ quỹ đạo bằng matplotlib (giao diện tương tác đẹp hơn)
    plot_orbit_interactive(x0_val, y0_val, phi_val)


if __name__ == "__main__":
    main()