import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../auth.service';

@Component({
  selector: 'app-esqueci-minha-senha',
  templateUrl: './esqueci-minha-senha.component.html',
  styleUrls: ['./esqueci-minha-senha.component.css']
})
export class EsqueciMinhaSenhaComponent {
  email: string = '';
  errorMessage: string = '';
  confirmationMessage: string = '';

  constructor( private router: Router, private authService: AuthService) {}

  forgotPassword() {
    if (!this.email) {
      this.errorMessage = 'Email não cadastrado. Por favor, insira um email válido.';
      return;
    }
    console.log(this.email);
    this.authService.forgotPassword(this.email).subscribe(
      (response) => {
        this.confirmationMessage = 'Email de redefinição de senha enviado! Verifique sua caixa de entrada.';
        this.errorMessage = '';
      },
      (error) => {
        console.log(error);
        this.errorMessage = 'Email não cadastrado. Por favor, insira um email válido.';
        this.confirmationMessage = '';
      }
    );

  }
}
