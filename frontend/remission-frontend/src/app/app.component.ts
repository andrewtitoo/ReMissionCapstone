import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FormsModule, CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'ReMission - Your IBD Management Companion';
  userId: string | null = null;
  userIdError: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.initializeUserId();
  }

  /**
   * Initializes the User ID.
   * Checks localStorage for an existing user_id. If not found, fetches from backend.
   */
  initializeUserId(): void {
    const storedUserId = localStorage.getItem('user_id');

    if (storedUserId) {
      this.userId = storedUserId;
      console.log(`Existing User ID loaded: ${this.userId}`);
    } else {
      this.autoAssignUserId(); // Only assign if not already present
    }
  }

  /**
   * Automatically assigns a new User ID from the backend and stores it.
   */
  autoAssignUserId(): void {
    this.apiService.autoAssignUser().subscribe(
      (response: any) => {
        this.userId = response.user_id;
        localStorage.setItem('user_id', this.userId); // Save to localStorage
        console.log(`New User ID assigned and stored: ${this.userId}`);
      },
      (error: any) => {
        this.userIdError = 'Failed to assign User ID. Please try refreshing.';
        console.error('Error auto-assigning User ID:', error);
      }
    );
  }

  /**
   * Logs the User ID to display it on the dashboard.
   */
  displayUserId(): string {
    return this.userId || 'Not assigned yet.';
  }
}
