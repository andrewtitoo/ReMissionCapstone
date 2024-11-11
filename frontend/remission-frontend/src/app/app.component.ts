import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'ReMission - Your IBD Management Companion';

  ngOnInit() {
    this.initializeUserId();
  }

  initializeUserId() {
    if (!localStorage.getItem('user_id')) {
      const userId = this.generateRandomUserId();
      localStorage.setItem('user_id', userId.toString());
      console.log(`New User ID Generated: ${userId}`);
    } else {
      console.log(`Existing User ID: ${localStorage.getItem('user_id')}`);
    }
  }

  generateRandomUserId(): number {
    return Math.floor(Math.random() * 100000);
  }
}
