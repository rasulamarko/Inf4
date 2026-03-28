import tkinter as tk
from tkinter import filedialog, messagebox
import base64

# Vrne abecedo glede na izbran jezik in velikost črk
def get_abeceda(jezik="en", velike_crke=False):
    if jezik == "sl":
        return "ABCČDEFGHIJKLMNOPRSŠTUVZŽ" if velike_crke else "abcčdefghijklmnoprsštuvzž"
    else:
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if velike_crke else "abcdefghijklmnopqrstuvwxyz"

# Poskusi zaznati jezik glede na posebne znake v besedilu
def zaznaj_jezik(besedilo):
    if any(c in besedilo.lower() for c in "čšž"):
        return "sl"
    return "en"

# Premakne znak za določen zamik v abecedi (Cezarjeva šifra)
def cezar_premik(znak, zamik, jezik):
    if not znak.isalpha():
        return znak

    velike = znak.isupper()
    abeceda = get_abeceda(jezik, velike_crke=velike)

    if znak not in abeceda:
        return znak

    indeks = abeceda.index(znak)
    nov_indeks = (indeks + zamik) % len(abeceda)
    return abeceda[nov_indeks]

# Šifriranje s Cezarjevo šifro
def cezar_sifriraj(besedilo, zamik, jezik="en"):
    return "".join(cezar_premik(c, zamik, jezik) for c in besedilo)


# Dešifriranje Cezarjeve šifre
def cezar_desifriraj(besedilo, zamik, jezik="en"):
    return cezar_sifriraj(besedilo, -zamik, jezik)

# Šifriranje z Vigenèrjevo šifro
def vigenere_sifriraj(besedilo, kljuc, jezik="en"):
    rezultat = ""
    kljuc = kljuc.lower()
    abeceda = get_abeceda(jezik)
    indeks_ključa = 0

    for znak in besedilo:
        if znak.lower() in abeceda:
            zamik = abeceda.index(kljuc[indeks_ključa % len(kljuc)].lower())
            rezultat += cezar_premik(znak, zamik, jezik)
            indeks_ključa += 1
        else:
            rezultat += znak
    return rezultat

# Dešifriranje Vigenèrjeve šifre
def vigenere_desifriraj(besedilo, kljuc, jezik="en"):
    rezultat = ""
    kljuc = kljuc.lower()
    abeceda = get_abeceda(jezik)
    indeks_ključa = 0

    for znak in besedilo:
        if znak.lower() in abeceda:
            zamik = -abeceda.index(kljuc[indeks_ključa % len(kljuc)].lower())
            rezultat += cezar_premik(znak, zamik, jezik)
            indeks_ključa += 1
        else:
            rezultat += znak
    return rezultat

# Šifriranje z XOR (vrne Base64)
def xor_sifriraj(besedilo, kljuc):
    if not kljuc:
        raise ValueError("Ključ za XOR ne sme biti prazen.")
    data = besedilo.encode('utf-8')
    key = kljuc.encode('utf-8')
    out = bytearray(len(data))
    for i in range(len(data)):
        out[i] = data[i] ^ key[i % len(key)]
    return base64.b64encode(bytes(out)).decode('ascii')

# Dešifriranje XOR (sprejme Base64 vhod)
def xor_desifriraj(besedilo_b64, kljuc):
    if not kljuc:
        raise ValueError("Ključ za XOR ne sme biti prazen.")
    try:
        data = base64.b64decode(besedilo_b64)
    except Exception:
        raise ValueError("Vhod ni veljaven Base64 za XOR dešifriranje.")
    key = kljuc.encode('utf-8')
    out = bytearray(len(data))
    for i in range(len(data)):
        out[i] = data[i] ^ key[i % len(key)]
    return out.decode('utf-8', errors='replace')

# Atbash šifra (obrne abecedo nazaj)
def atbash_sifriraj(besedilo, jezik="en"):
    rezultat = []
    abec = get_abeceda(jezik)
    rev = abec[::-1]
    abec_upper = get_abeceda(jezik, velike_crke=True)
    rev_upper = abec_upper[::-1]

    for c in besedilo:
        if c in abec:
            rezultat.append(rev[abec.index(c)])
        elif c in abec_upper:
            rezultat.append(rev_upper[abec_upper.index(c)])
        else:
            rezultat.append(c)
    return "".join(rezultat)

# ROT13 (posebni primer Cezarja za angleščino; za slovenski je uporabljen polovica abecede)
def rot13_sifriraj(besedilo, jezik="en"):
    if jezik == "en":
        return cezar_sifriraj(besedilo, 13, jezik)
    else:
        # uporabimo polovico slovenske abecede (najbližje ROT13)
        n = len(get_abeceda("sl"))
        return cezar_sifriraj(besedilo, n // 2, "sl")

# Base64 kodiranje/dekodiranje
def base64_encode(besedilo):
    return base64.b64encode(besedilo.encode('utf-8')).decode('ascii')

def base64_decode(besedilo_b64):
    try:
        return base64.b64decode(besedilo_b64).decode('utf-8', errors='replace')
    except Exception:
        raise ValueError("Neveljaven Base64 vhod.")

# Naloži besedilo iz datoteke v vnosno polje
def nalozi_datoteko():
    pot = filedialog.askopenfilename()
    if pot:
        with open(pot, 'r', encoding='utf-8') as f:
            vsebina = f.read()
            vnosno_besedilo.delete("1.0", tk.END)
            vnosno_besedilo.insert(tk.END, vsebina)
        jezik.set(zaznaj_jezik(vsebina))

# Shrani rezultat v izbrano datoteko
def shrani_datoteko():
    pot = filedialog.asksaveasfilename(defaultextension=".txt")
    if pot:
        with open(pot, 'w', encoding='utf-8') as f:
            f.write(izhodno_besedilo.get("1.0", tk.END).strip())
        messagebox.showinfo("Shranjeno", f"Rezultat je bil shranjen v: {pot}")

# Izvede šifriranje ali dešifriranje glede na izbrane nastavitve
def izvedi_sifro():
    besedilo = vnosno_besedilo.get("1.0", tk.END).strip()
    kljuc = kljuc_vnos.get()
    metoda = metoda_var.get()
    jezik_izbran = jezik.get()
    nacin = nacin_var.get()

    if not besedilo:
        messagebox.showerror("Napaka", "Vnosno besedilo je prazno!")
        return

    try:
        if metoda == "Cezar":
            try:
                zamik = int(kljuc)
            except Exception:
                messagebox.showerror("Napaka", "Za Cezarjevo šifro mora biti ključ cel številka.")
                return
            rezultat = cezar_sifriraj(besedilo, zamik, jezik_izbran) if nacin == "Šifriraj" else cezar_desifriraj(besedilo, zamik, jezik_izbran)
        elif metoda == "Vigenere":
            if not kljuc:
                messagebox.showerror("Napaka", "Vnesite ključ za Vigenère.")
                return
            rezultat = vigenere_sifriraj(besedilo, kljuc, jezik_izbran) if nacin == "Šifriraj" else vigenere_desifriraj(besedilo, kljuc, jezik_izbran)
        elif metoda == "XOR":
            if not kljuc:
                messagebox.showerror("Napaka", "Vnesite ključ za XOR.")
                return
            if nacin == "Šifriraj":
                rezultat = xor_sifriraj(besedilo, kljuc)
            else:
                rezultat = xor_desifriraj(besedilo, kljuc)
        elif metoda == "Atbash":
            rezultat = atbash_sifriraj(besedilo, jezik_izbran)
        elif metoda == "ROT13":
            rezultat = rot13_sifriraj(besedilo, jezik_izbran)
        elif metoda == "Base64":
            if nacin == "Šifriraj":
                rezultat = base64_encode(besedilo)
            else:
                rezultat = base64_decode(besedilo)
        else:
            messagebox.showerror("Napaka", "Neznana metoda.")
            return

        izhodno_besedilo.delete("1.0", tk.END)
        izhodno_besedilo.insert(tk.END, rezultat)
    except Exception as e:
        messagebox.showerror("Napaka", str(e))

# Nastavitve in postavitev grafičnega vmesnika (GUI)
root = tk.Tk()
root.title("Šifriranje besedila")
root.resizable(True, True)

# Konfiguracija mreže
for i in range(4):  # 4 stolpci
    root.columnconfigure(i, weight=1)
for i in range(8):  # 8 vrstic
    root.rowconfigure(i, weight=1)

# Vnosno polje za besedilo
tk.Label(root, text="Vhodno besedilo:").grid(row=0, column=0, sticky="w")
vnosno_besedilo = tk.Text(root, height=10, wrap="word")
vnosno_besedilo.grid(row=1, column=0, columnspan=4, sticky="nsew")

# Gumbi za nalaganje in shranjevanje datotek
tk.Button(root, text="Naloži datoteko", command=nalozi_datoteko).grid(row=2, column=0, sticky="ew")
tk.Button(root, text="Shrani rezultat", command=shrani_datoteko).grid(row=2, column=1, sticky="ew")

# Izbira načina (šifriranje/dešifriranje)
tk.Label(root, text="Način:").grid(row=3, column=0, sticky="e")
nacin_var = tk.StringVar(value="Šifriraj")
tk.OptionMenu(root, nacin_var, "Šifriraj", "Dešifriraj").grid(row=3, column=1, sticky="ew")

# Izbira metode šifriranja
tk.Label(root, text="Metoda:").grid(row=3, column=2, sticky="e")
metoda_var = tk.StringVar(value="Cezar")
tk.OptionMenu(root, metoda_var, "Cezar", "Vigenere", "XOR", "Atbash", "ROT13", "Base64").grid(row=3, column=3, sticky="ew")

# Izbira jezika (sl/en)
tk.Label(root, text="Jezik:").grid(row=4, column=0, sticky="e")
jezik = tk.StringVar(value="en")
tk.OptionMenu(root, jezik, "sl", "en").grid(row=4, column=1, sticky="ew")

# Vnos ključa ali zamika
tk.Label(root, text="Ključ / zamik:").grid(row=4, column=2, sticky="e")
kljuc_vnos = tk.Entry(root)
kljuc_vnos.grid(row=4, column=3, sticky="ew")

# Gumb za izvedbo šifriranja/dešifriranja
tk.Button(root, text="Zaženi", command=izvedi_sifro, bg="lightblue").grid(row=5, column=1, columnspan=2, sticky="ew")

# Izhodno polje za rezultat
tk.Label(root, text="Izhodno besedilo:").grid(row=6, column=0, sticky="w")
izhodno_besedilo = tk.Text(root, height=10, wrap="word")
izhodno_besedilo.grid(row=7, column=0, columnspan=4, sticky="nsew")

root.mainloop()