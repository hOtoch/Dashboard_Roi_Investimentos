import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { LoginResponse } from './models/login-response.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/login';  // URL da API Flask
  private tokenKey = 'token';  // Chave do token no localStorage
  private userIdKey = 'userId';  // Chave do ID do usuário no localStorage

  constructor(private http: HttpClient) {}

  login(data: { email: string; senha: string }): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.apiUrl, data).pipe(
      tap((response: LoginResponse) => {
        // Armazenar o token e o ID do usuário no localStorage após o login bem-sucedido
        localStorage.setItem(this.tokenKey, response.access_token);
        localStorage.setItem(this.userIdKey, response.user_id.toString());
      })
    );
  }

  // Método para obter o token do localStorage
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  // Método para obter o ID do usuário do localStorage
  getUserId(): string | null {
    return localStorage.getItem(this.userIdKey);
  }

  // Método para remover o token e o ID do usuário do localStorage (logout)
  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userIdKey);
  }

  // Verifica se o usuário está autenticado
  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}
