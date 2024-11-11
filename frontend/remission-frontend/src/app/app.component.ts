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
  userId: number | null = null;

  ngOnInit(): void {
    this.initializeUserId();
  }

  initializeUserId(): void {
    const storedUserId = localStorage.getItem('user_id');
    if (!storedUserId) {
      this.userId = this.generateRandomUserId();
      localStorage.setItem('user_id', this.userId.toString());
      console.log(`New User ID Generated: ${this.userId}`);
    } else {
      this.userId = parseInt(storedUserId, 10);
      console.log(`Existing User ID: ${this.userId}`);
    }
  }

  generateRandomUserId(): number {
    return Math.floor(10000 + Math.random() * 90000); // 5-digit unique ID
  }
}
