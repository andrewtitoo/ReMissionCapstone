import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'ReMission - Your IBD Management Companion';
  userId: string | null = null;
  userIdError: string = '';

  constructor(
    private apiService: ApiService,
    @Inject(PLATFORM_ID) private platformId: object
  ) {}

  ngOnInit(): void {
    this.initializeUserId();
  }

  /**
   * Initializes the User ID.
   * Checks localStorage for an existing user_id if running in the browser.
   */
  initializeUserId(): void {
    if (isPlatformBrowser(this.platformId)) {
      const storedUserId = localStorage.getItem('user_id');

      if (storedUserId) {
        this.userId = storedUserId;
        console.log(`Existing User ID loaded: ${this.userId}`);
      } else {
        this.autoAssignUserId();
      }
    } else {
      console.log('Not running in the browser, skipping localStorage access.');
    }
  }

  /**
   * Automatically assigns a new User ID from the backend and stores it.
   */
  autoAssignUserId(): void {
    this.apiService.autoAssignUser().subscribe(
      (response: any) => {
        this.userId = response.user_id;
        if (isPlatformBrowser(this.platformId)) {
          localStorage.setItem('user_id', this.userId);
        }
        console.log(`New User ID assigned and stored: ${this.userId}`);
      },
      (error: any) => {
        this.userIdError = 'Failed to assign User ID. Please try refreshing.';
        console.error('Error auto-assigning User ID:', error);
      }
    );
  }

  displayUserId(): string {
    return this.userId || 'Not assigned yet.';
  }
}
