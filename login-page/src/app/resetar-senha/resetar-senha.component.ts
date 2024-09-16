import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-resetar-senha',
  templateUrl: './resetar-senha.component.html',
  styleUrls: ['./resetar-senha.component.css']
})
export class ResetarSenhaComponent implements OnInit{
  newPassword: string = '';
  token: string = '';
  errorMessage: string = '';
  confirmationMessage: string = '';

  constructor(private authService: AuthService, private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    // Obtém o token da URL
    this.token = this.route.snapshot.params['token'];
  }

  resetPassword() {
    // Envia a nova senha e o token para o backend
    this.authService.resetPassword(this.token, this.newPassword).subscribe(
      (response) => {
        this.confirmationMessage = 'Senha redefinida com sucesso!';
        this.errorMessage = '';
      },
      (error) => {
        this.errorMessage = 'Falha ao redefinir senha. Verifique o token ou tente novamente.';
        this.confirmationMessage = '';
      }
    );
  }
}
