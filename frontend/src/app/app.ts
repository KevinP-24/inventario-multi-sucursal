import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { AuthSessionService } from './core/services/auth/auth-session.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private readonly authSession = inject(AuthSessionService);

  constructor() {
    this.authSession.restoreSession().subscribe();
  }
}
