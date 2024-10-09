import sqlite3
import hashlib
import os
import time

class Database:
    def __init__(self, db_name='../data/truco_ranker01.db'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, db_name)

        # Verificar se o caminho está correto
        print(f"Tentando acessar o banco de dados em: {db_path}")

        # Garantir que o diretório existe
        if not os.path.exists(os.path.dirname(db_path)):
            print("Diretório do banco de dados não existe. Criando...")
            os.makedirs(os.path.dirname(db_path))  # Cria o diretório, se necessário

        self.connect_to_database(db_path)

    def connect_to_database(self, db_path):
        """Tenta conectar ao banco de dados, reestabelecendo a conexão se estiver bloqueado."""
        attempt = 0
        while attempt < 5:  # Tenta conectar 5 vezes
            try:
                # Conectar ao banco de dados com timeout de 5 segundos e busy_timeout de 10 segundos
                self.conn = sqlite3.connect(db_path, timeout=5)
                self.conn.execute("PRAGMA busy_timeout = 10000")  # Espera até 10 segundos se o DB estiver ocupado
                # Remover o PRAGMA WAL temporariamente se estiver causando problemas
                # self.conn.execute("PRAGMA journal_mode=WAL")  # Ativa o Write-Ahead Logging (comentado temporariamente)
                self.cursor = self.conn.cursor()
                self.create_tables()
                print("Conexão ao banco de dados estabelecida com sucesso.")
                break  # Sai do loop se a conexão foi bem-sucedida
            except sqlite3.OperationalError as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                attempt += 1
                time.sleep(2)  # Espera 2 segundos antes de tentar novamente

        if attempt == 5:
            raise Exception("Não foi possível conectar ao banco de dados após várias tentativas.")

    def create_tables(self):
        try:
            self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,  
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(user_id),
                score INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS tournaments (
                tournament_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                code TEXT NOT NULL UNIQUE,
                creator_user_id INTEGER REFERENCES users(user_id),
                rule INTEGER NOT NULL DEFAULT 1  -- Adiciona o campo de regra (1 ou 2)
            );

            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER REFERENCES tournaments(tournament_id),
                match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS match_players (
                match_id INTEGER REFERENCES matches(match_id),
                player_id INTEGER REFERENCES players(player_id),
                tournament_id INTEGER REFERENCES tournaments(tournament_id),
                score INTEGER DEFAULT 0,
                PRIMARY KEY (match_id, player_id)
            );
            ''')
            self.conn.commit()
            print("Tabelas criadas com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")
            self.conn.rollback()

    def create_user(self, username, email, password, name):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute(
                "INSERT INTO users (username, email, password_hash, name) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, name)
            )
            user_id = self.cursor.lastrowid
            self.cursor.execute(
                "INSERT INTO players (user_id, score) VALUES (?, 0)", (user_id,)
            )
            self.conn.commit()
            print("Usuário criado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar usuário: {e}")
            self.conn.rollback()

    def create_tournament(self, name, code, creator_user_id):
        try:
            self.cursor.execute(
                "INSERT INTO tournaments (name, code, creator_user_id) VALUES (?, ?, ?)",
                (name, code, creator_user_id)
            )
            self.conn.commit()
            print("Torneio criado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar torneio: {e}")
            self.conn.rollback()

    def create_match(self, tournament_id):
        try:
            self.cursor.execute(
                "INSERT INTO matches (tournament_id) VALUES (?)", (tournament_id,)
            )
            match_id = self.cursor.lastrowid
            self.conn.commit()
            print("Partida criada com sucesso.")
            return match_id
        except sqlite3.Error as e:
            print(f"Erro ao criar partida: {e}")
            self.conn.rollback()

    def add_player_to_match(self, match_id, player_id, tournament_id, score=0):
        try:
            self.cursor.execute(
                "INSERT INTO match_players (match_id, player_id, tournament_id, score) VALUES (?, ?, ?, ?)",
                (match_id, player_id, tournament_id, score)
            )
            self.conn.commit()
            print("Jogador adicionado à partida com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao adicionar jogador à partida: {e}")
            self.conn.rollback()

    def update_score(self, player_id, score, match_id=None):
        try:
            if match_id:
                self.cursor.execute(
                    "UPDATE match_players SET score = score + ? WHERE player_id = ? AND match_id = ?",
                    (score, player_id, match_id)
                )
            else:
                self.cursor.execute(
                    "UPDATE players SET score = score + ? WHERE player_id = ?", (score, player_id)
                )
            self.conn.commit()
            print("Pontuação atualizada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao atualizar pontuação: {e}")
            self.conn.rollback()

    def authenticate_user(self, username, password):
        """Verifica se a conexão está ativa e autentica o usuário."""
        if not hasattr(self, 'cursor'):
            raise Exception("Erro: O banco de dados não foi conectado corretamente.")
        
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao autenticar usuário: {e}")
            return None

    def get_user_by_username(self, username):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar usuário: {e}")

    def get_player_id(self, user_id):
        try:
            self.cursor.execute("SELECT player_id FROM players WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar ID do jogador: {e}")

    def update_password(self, email, new_password):
        try:
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            self.cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (password_hash, email))
            self.conn.commit()
            print("Senha atualizada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao atualizar senha: {e}")
            self.conn.rollback()

    def close(self):
        try:
            if self.conn:
                self.conn.close()
                print("Conexão com o banco de dados fechada.")
        except sqlite3.Error as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {e}")
