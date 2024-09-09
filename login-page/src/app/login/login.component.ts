import { Component,OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { LoginResponse } from '../models/login-response.model';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements AfterViewInit{
  email: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) { }

  @ViewChild('videoBackground', { static: false }) videoRef?: ElementRef<HTMLVideoElement>;

  ngAfterViewInit(): void {
    // Aguarda a primeira interação do usuário para iniciar o vídeo
    document.body.addEventListener('click', () => {
      this.playVideo();
    }, { once: true }); // Adiciona o evento apenas uma vez
  }


  playVideo(): void {
    if (this.videoRef) {
      const video = this.videoRef.nativeElement;
      video.currentTime = 0; // Reinicia o vídeo do início
      video.muted = true; // Garante que o vídeo esteja sem som
      video.play().catch(error => {
        console.error('Erro ao tentar reproduzir o vídeo:', error);
      });
    }
  }

  login() {
    const loginData = {
      email: this.email,
      senha: this.password
    };

    this.authService.login(loginData).subscribe(
      (response: LoginResponse) => {  

        console.log(this.authService.getToken())
        console.log(this.authService.getUserId())
        // this.router.navigate(['/dashboard']); 
        this.errorMessage = '';
      },
      (error) => {
        console.error('Erro ao autenticar', error);
        this.errorMessage = 'Dados de login inválidos';
      }
    );
  }
}
