import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { Router } from '@angular/router';

import { AuthSessionService } from '../../../core/services/auth/auth-session.service';

@Component({
  selector: 'app-login-page',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.page.html',
  styleUrl: './login.page.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginPage {
  private readonly formBuilder = inject(FormBuilder);
  private readonly authSession = inject(AuthSessionService);
  private readonly router = inject(Router);

  protected readonly isSubmitting = signal(false);
  protected readonly isPasswordVisible = signal(false);
  protected readonly submitError = signal<string | null>(null);
  protected readonly eyeIconPath = faEye.icon[4] as string;
  protected readonly eyeSlashIconPath = faEyeSlash.icon[4] as string;

  protected readonly loginForm = this.formBuilder.nonNullable.group({
    correo: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]]
  });

  protected submit() {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    const rawValue = this.loginForm.getRawValue();
    const credentials = {
      correo: rawValue.correo.trim().toLowerCase(),
      password: rawValue.password.trim()
    };

    this.isSubmitting.set(true);
    this.submitError.set(null);

    this.authSession.login(credentials).subscribe({
      next: () => {
        this.isSubmitting.set(false);
        void this.router.navigate(['/app/dashboard']);
      },
      error: (error: HttpErrorResponse) => {
        this.isSubmitting.set(false);
        this.submitError.set(this.resolveLoginError(error));
      }
    });
  }

  protected togglePasswordVisibility() {
    this.isPasswordVisible.update((visible) => !visible);
  }

  private resolveLoginError(error: HttpErrorResponse): string {
    const apiError = error.error as { errors?: Record<string, string>; message?: string } | null;

    if (apiError?.errors?.['credenciales']) {
      return apiError.errors['credenciales'];
    }

    if (apiError?.errors?.['usuario']) {
      return apiError.errors['usuario'];
    }

    if (apiError?.message) {
      return apiError.message;
    }

    return 'No se pudo iniciar sesion. Verifica tus credenciales e intenta nuevamente.';
  }
}
