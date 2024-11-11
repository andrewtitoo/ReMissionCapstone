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

  /**
   * Initializes the user ID for the current session.
   * Checks localStorage for an existing ID or generates a new one.
   */
  initializeUserId(): void {
    const storedUserId = this.getUserIdFromLocalStorage();
    if (storedUserId) {
      this.userId = storedUserId;
      console.log(`Existing User ID: ${this.userId}`);
    } else {
      this.userId = this.generateRandomUserId();
      this.storeUserIdInLocalStorage(this.userId);
      console.log(`New User ID Generated: ${this.userId}`);
    }
  }

  /**
   * Retrieves the user ID from localStorage.
   * @returns {number | null} The stored user ID or null if not found.
   */
  getUserIdFromLocalStorage(): number | null {
    const userId = localStorage.getItem('user_id');
    return userId ? parseInt(userId, 10) : null;
  }

  /**
   * Stores the generated user ID in localStorage.
   * @param userId The user ID to store.
   */
  storeUserIdInLocalStorage(userId: number): void {
    localStorage.setItem('user_id', userId.toString());
  }

  /**
   * Generates a random 5-digit user ID.
   * @returns {number} The generated user ID.
   */
  generateRandomUserId(): number {
    return Math.floor(10000 + Math.random() * 90000);
  }
}
