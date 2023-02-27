from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
GUI = Builder.load_file('tela.kv')
antena_selecionada = [0]
gerando = [False]
class MeuApp(App):
    def build(self):
        self.title = 'CS_TV'
        box = BoxLayout(orientation='vertical')
        botao = Button(text='Gerar', font_size=20, on_release=self.gerar)
        self.titulo = Label(text='Escolha sua Antena:')
        self.claro = Button(text='CLARO TV', font_size=15, on_release=self.antena)
        self.sky = Button(text='SKY', font_size=15, on_release=self.antena)
        self.cs_tv = Label(text='\n\n\n\n\n\nSeu CS será gerado aqui:')
        box.add_widget(self.titulo)
        box.add_widget(self.claro)
        box.add_widget(self.sky)
        box.add_widget(botao)
        box.add_widget(self.cs_tv)
        box.add_widget(Label(text=''))
        box.add_widget(Label(text=''))
        return box
    def antena(self, antena):
        if gerando[0] == False:
            if antena.text == 'CLARO TV':
                self.sky.background_color = 1, 1, 1
                antena_selecionada[0] = 18
                self.claro.background_color = 255, 215, 0
            elif antena.text == 'SKY':
                self.claro.background_color = 1, 1, 1
                antena_selecionada[0] = 19
                self.sky.background_color = 255, 215, 0
            print(antena_selecionada[0])
    def gerar(self, botao):
        if gerando[0] == False:
            gerando[0] = True
            import subprocess
            from playwright.sync_api import sync_playwright
            subprocess.run(['playwright', 'install', 'chromium'])
            from time import sleep
            with sync_playwright() as pw:
                navegador = pw.chromium.launch()
                email_temporario = navegador.new_page()
                email_temporario.set_default_timeout(120000)  # Esperar no máximo 2 minutos
                email_temporario.goto('https://pt.emailfake.com/')  # Acessar o Site
                pegar_dados_email = str(email_temporario.content())
                pegar_email = pegar_dados_email.split('<span id="email_ch_text">')
                separar_email = pegar_email[1]
                caracteres = separar_email.find('<')
                email = separar_email[0:caracteres]
                cs_goias = navegador.new_page()
                cs_goias.goto('http://superpainel.mine.nu/painel/formulario_testes.php?r=SGJtd0pmNXd1TTlzRUNtT25JK0lTallkL1RQVnBTMkFBQXMrWnlsZXEvdz0,')  # Teste 48H Cs
                cs_goias.fill('xpath=/html/body/div/div/form/div[1]/input', 'User')  # Preencher Nome
                cs_goias.fill('xpath=/html/body/div/div/form/div[2]/input', f'{email}')  # Preencher Email
                cs_goias.locator(f'xpath=/html/body/div/div/form/div[3]/div[{antena_selecionada[0]}]/input').click()  # Claro Tv Hd / Sky
                cs_goias.locator('xpath=/html/body/div/div/form/div[4]/button').click()  # Enviar
                sleep(5)
                email_temporario.reload()
                dados = str(email_temporario.content())
                separar_vencimento = dados.split('Vencimento: ')
                vencimento = separar_vencimento[1]
                separar_usuario = dados.split('login / usuario:&nbsp;')
                usuario = separar_usuario[1]
                fim_usuario = usuario.find('<')
                separar_senha = dados.split('Senha / password: ')
                senha = separar_senha[1]
                self.cs_tv.text = f'\n\n\n\n\n\nVencimento: {vencimento[0:19]}\nNome de Usuário: User\nUsuário / Login: {usuario[0:fim_usuario]}\nSenha / Password: {senha[0:3]}\nDADOS DO SERVIDOR:\nClaro Tv\nUrl / Ip: csgoias.ddns.net\nPorta: 32005\nChave DES: 01 02 03 04 05 06 07 08 09 10 11 12 13 14' if antena_selecionada[0] == 18 else f'\n\n\n\n\n\nVencimento: {vencimento[0:19]}\nNome de Usuário: User\nUsuário / Login: {usuario[0:fim_usuario]}\nSenha / Password: {senha[0:3]}\nDADOS DO SERVIDOR:\nSky\nUrl / Ip: csgoias.ddns.net\nPorta: 31005\nChave DES: 01 02 03 04 05 06 07 08 09 10 11 12 13 14'
                gerando[0] = False


MeuApp().run()
