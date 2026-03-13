from inventario import Inventario, Articulo

DATA = [
    Articulo("BMW-0001", "Filtro de aceite OEM (N52/N54)", 180.00, 320.00, 290.00, "Motor", "BMW", "OEM", 6, 18, 24),
    Articulo("BMW-0002", "Bujía Iridium (N20/N26)", 210.00, 380.00, 350.00, "Motor", "BMW", "OEM", 6, 40, 36),
    Articulo("BMW-0003", "Sensor MAF (E90/E92)", 1450.00, 2100.00, 1950.00, "Motor", "BMW", "OEM", 12, 5, 48),
    Articulo("BMW-0004", "Bomba de agua eléctrica (N52)", 3200.00, 4800.00, 4500.00, "Motor", "BMW", "OEM", 12, 2, 60),
    Articulo("BMW-0005", "Termostato (N52)", 1250.00, 1950.00, 1800.00, "Motor", "BMW", "OEM", 12, 3, 60),
    Articulo("BMW-0006", "Banda serpentina (E60/E90)", 420.00, 690.00, 640.00, "Motor", "BMW", "OEM", 6, 12, 36),
    Articulo("BMW-0010", "Balata delantera (E90)", 980.00, 1650.00, 1550.00, "Frenos", "BMW", "OEM", 6, 9, 18),
    Articulo("BMW-0011", "Disco de freno delantero (E90)", 1250.00, 2100.00, 1950.00, "Frenos", "BMW", "OEM", 6, 8, 24),
    Articulo("BMW-0012", "Sensor ABS (E90)", 720.00, 1250.00, 1180.00, "Frenos", "BMW", "OEM", 12, 6, 48),
    Articulo("BMW-0020", "Amortiguador delantero (E90)", 2100.00, 3450.00, 3200.00, "Suspensión", "BMW", "OEM", 12, 4, 48),
    Articulo("BMW-0021", "Brazo de control (E90)", 1350.00, 2200.00, 2050.00, "Suspensión", "BMW", "OEM", 12, 6, 48),
    Articulo("BMW-0022", "Buje de suspensión (E90)", 380.00, 680.00, 630.00, "Suspensión", "BMW", "OEM", 6, 15, 36),
    Articulo("BMW-0023", "Terminal de dirección (E90)", 520.00, 920.00, 860.00, "Suspensión", "BMW", "OEM", 6, 10, 36),
    Articulo("BMW-0030", "Aceite 5W-30 Longlife (1L)", 190.00, 320.00, 300.00, "Aditivos", "BMW", "OEM", 0, 55, 24),
    Articulo("BMW-0031", "Anticongelante BMW (1L)", 210.00, 350.00, 330.00, "Aditivos", "BMW", "OEM", 0, 30, 36),
    Articulo("BMW-0032", "Líquido de frenos DOT 4 (500ml)", 140.00, 240.00, 220.00, "Aditivos", "BMW", "OEM", 0, 22, 24),
    Articulo("BMW-0040", "Filtro de aire (E90)", 320.00, 520.00, 480.00, "Filtros", "BMW", "OEM", 6, 14, 24),
    Articulo("BMW-0041", "Filtro de cabina (E90)", 280.00, 480.00, 440.00, "Filtros", "BMW", "OEM", 6, 20, 24),
    Articulo("BMW-0050", "Batería AGM 90Ah", 3600.00, 5200.00, 4950.00, "Eléctrico", "BMW", "OEM", 12, 1, 48),
    Articulo("BMW-0051", "Bobina de encendido (N20)", 680.00, 1150.00, 1080.00, "Eléctrico", "BMW", "OEM", 12, 7, 36),
    Articulo("BMW-0098", "Sensor de oxígeno (pre-cat)", 1650.00, 2550.00, 2400.00, "Motor", "BMW", "OEM", 12, 0, 48),
    Articulo("BMW-0099", "Manguera radiador superior", 490.00, 820.00, 780.00, "Motor", "BMW", "OEM", 6, 2, 36),
]


def main():
    inv = Inventario("inventario.db")
    inv.cargar()
    existing = {it.id for it in inv.items}
    added = 0
    for a in DATA:
        if a.id in existing:
            continue
        inv.agregar(a)
        added += 1
    print(f"Listo: se agregaron {added} artículos (si ya existían, se saltaron).")


if __name__ == "__main__":
    main()