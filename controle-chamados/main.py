import time
import json
from datetime import timedelta
import tkinter as tk
from tkinter import messagebox

ARQUIVO_JSON = "chamados.json"

class Chamado:
    def __init__(self, id, descricao, status="Aguardando", tempo_gasto=0, inicio=None):
        self.id = id
        self.descricao = descricao
        self.status = status
        self.tempo_gasto = timedelta(seconds=tempo_gasto)
        self.inicio = inicio
    
    def iniciar(self):
        if self.status == "Em andamento":
            messagebox.showinfo("Aviso", "Chamado já está em andamento.")
            return
        self.status = "Em andamento"
        self.inicio = time.time()
    
    def parar(self):
        if self.status != "Em andamento":
            messagebox.showinfo("Aviso", "Chamado não está em andamento.")
            return
        tempo_decorrido = time.time() - self.inicio
        self.tempo_gasto += timedelta(seconds=tempo_decorrido)
        self.status = "Aguardando"
        self.inicio = None
    
    def finalizar(self):
        if self.status == "Em andamento":
            self.parar()
        self.status = "Finalizado"
    
    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "status": self.status,
            "tempo_gasto": self.tempo_gasto.total_seconds(),
            "inicio": self.inicio
        }
    
    @staticmethod
    def from_dict(data):
        return Chamado(data["id"], data["descricao"], data["status"], data["tempo_gasto"], data["inicio"])
    
    def __str__(self):
        return f"{self.id}: {self.descricao} | Status: {self.status} | Tempo: {self.tempo_gasto}"  

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Chamados")
        
        self.chamados = self.carregar_chamados()
        
        # Elementos da interface
        tk.Label(root, text="ID:").grid(row=0, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Descrição:").grid(row=1, column=0)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=1, column=1)
        
        tk.Button(root, text="Adicionar Chamado", command=self.adicionar_chamado).grid(row=2, column=0, columnspan=2)
        
        self.lista_chamados = tk.Listbox(root, width=50)
        self.lista_chamados.grid(row=3, column=0, columnspan=2)
        
        tk.Button(root, text="Iniciar", command=self.iniciar_chamado).grid(row=4, column=0)
        tk.Button(root, text="Parar", command=self.parar_chamado).grid(row=4, column=1)
        tk.Button(root, text="Finalizar", command=self.finalizar_chamado).grid(row=5, column=0, columnspan=2)
        
        self.atualizar_lista()
    
    def adicionar_chamado(self):
        id = self.id_entry.get()
        descricao = self.desc_entry.get()
        if id in self.chamados:
            messagebox.showerror("Erro", "Chamado com esse ID já existe.")
            return
        self.chamados[id] = Chamado(id, descricao)
        self.salvar_chamados()
        self.atualizar_lista()
    
    def iniciar_chamado(self):
        id = self.get_chamado_selecionado()
        if id:
            self.chamados[id].iniciar()
            self.salvar_chamados()
            self.atualizar_lista()
    
    def parar_chamado(self):
        id = self.get_chamado_selecionado()
        if id:
            self.chamados[id].parar()
            self.salvar_chamados()
            self.atualizar_lista()
    
    def finalizar_chamado(self):
        id = self.get_chamado_selecionado()
        if id:
            self.chamados[id].finalizar()
            self.salvar_chamados()
            self.atualizar_lista()
    
    def get_chamado_selecionado(self):
        try:
            selecionado = self.lista_chamados.get(self.lista_chamados.curselection())
            return selecionado.split(":")[0]
        except:
            messagebox.showerror("Erro", "Selecione um chamado.")
            return None
    
    def atualizar_lista(self):
        self.lista_chamados.delete(0, tk.END)
        for chamado in self.chamados.values():
            self.lista_chamados.insert(tk.END, str(chamado))
    
    def salvar_chamados(self):
        with open(ARQUIVO_JSON, "w") as f:
            json.dump({id: chamado.to_dict() for id, chamado in self.chamados.items()}, f, indent=4)
    
    def carregar_chamados(self):
        try:
            with open(ARQUIVO_JSON, "r") as f:
                dados = json.load(f)
                return {id: Chamado.from_dict(dados[id]) for id in dados}
        except FileNotFoundError:
            return {}
    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
