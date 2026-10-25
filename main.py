import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    # TITOLO pagina
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Pulsante per cambiare tema
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label='Tipo', expand=True) # L'istruzione label crea la scritta guida dentro la casella (sparisce quando scrivi)
    input_marca = ft.TextField(label='Marca', expand=True)
    input_anno = ft.TextField(label='Anno Acquisto', expand=True)

    # Variabile e testo per il contatore del valore in euro
    valore_corrente = 0
    txt_valore = ft.Text(value='0', size=16, weight=ft.FontWeight.BOLD)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        # Pulisce la lista e la ricarica ordinata per marca
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP --- (gestiti al click)
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # Gestione del contatore
    def incrementa_valore(e):
        nonlocal valore_corrente # Permette di modificare la variabile esterna alla funzione
        valore_corrente += 10
        txt_valore.value = str(valore_corrente)
        txt_valore.update()

    def decrementa_valore(e):
        nonlocal valore_corrente # Permette di modificare la variabile esterna alla funzione
        if valore_corrente >= 10:
            valore_corrente -= 10
            txt_valore.value = str(valore_corrente)
            txt_valore.update()

    def aggiungi_strumento_handler(e):
        nonlocal valore_corrente
        try:
            tipo = input_tipo.value
            marca = input_marca.value

            if not tipo or not marca:
                alert.show_alert('Errore: I campi Tipo e Marca non possono essere vuoti')
                return  # Interrompe l'esecuzione della funzione

            anno = int(input_anno.value)
            valore = float(valore_corrente)

            # Aggiunge lo strumento tramite la logica del Lab03
            deposito.aggiungi_strumento(tipo, marca, anno, valore)

            # Svuota i campi e resetta il contatore dopo l'inserimento
            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            valore_corrente = 0
            txt_valore.value = "0"
            txt_valore.update()
            # Una volta che l'utente ha digitato i dati di un nuovo strumento e ha cliccato su "Aggiungi strumento",
            # quelle informazioni sono state correttamente elaborate e salvate nel deposito.
            # Se non svuotassimo le caselle, i dati dello strumento appena inserito rimarrebbero scritti dentro i campi.
            # Questo significherebbe che, se l'utente volesse inserire un secondo strumento,
            # dovrebbe prima cancellare a mano tutto quello che c'era scritto prima.
            # Svuotandoli subito dopo il salvataggio, invece, la schermata torna pulita e pronta per un eventuale nuovo inserimento,
            # evitando anche il rischio di aggiungere per errore lo stesso strumento due volte!

            aggiorna_lista_strumenti()
            page.update()

        except ValueError: # Se l'utente sbaglia a scrivere
            alert.show_alert('Errore nei dati inseriti')


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btn_meno = ft.Button('-', color='red', on_click=decrementa_valore)
    btn_piu = ft.Button('+', color='green', on_click=incrementa_valore)
    pulsante_aggiungi_strumento = ft.Button('Aggiungi Strumento', on_click=aggiungi_strumento_handler)

    # RIGHE DI LAYOUT (ft.Row) per ordinare i campi
    row_campi_strumento = ft.Row(
        controls=[input_tipo, input_marca, input_anno, btn_meno, txt_valore, btn_piu],
        alignment=ft.MainAxisAlignment.CENTER
    )
    row_pulsante_aggiungi = ft.Row([pulsante_aggiungi_strumento], alignment=ft.MainAxisAlignment.CENTER)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text('Aggiungi Nuovo Strumento', size=20),
        row_campi_strumento,
        row_pulsante_aggiungi,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()
    page.update()

ft.run(main)
