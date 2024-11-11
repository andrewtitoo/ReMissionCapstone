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
  userIdInput: string = ''; // Store user input temporarily

  ngOnInit(): void {
    this.promptForUserId();
  }

  /**
   * Prompts the user to enter their User ID or creates a new one.
   */
  promptForUserId(): void {
    const storedUserId = this.getUserIdFromLocalStorage();
    if (storedUserId) {
      this.userId = storedUserId;
      console.log(`Welcome back! Your User ID is: ${this.userId}`);
    } else {
      // User needs to input their User ID manually
      alert('Please enter your User ID or create a new one.');
    }
  }

  /**
   * Confirms and stores the entered User ID.
   */
  confirmUserId(): void {
    if (this.userIdInput) {
      this.userId = parseInt(this.userIdInput, 10);
      this.storeUserIdInLocalStorage(this.userId);
      console.log(`User ID confirmed: ${this.userId}`);
    } else {
      alert('Invalid User ID. Please try again.');
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
   * Stores the user ID in localStorage.
   * @param userId The user ID to store.
   */
  storeUserIdInLocalStorage(userId: number): void {
    localStorage.setItem('user_id', userId.toString());
  }
}
