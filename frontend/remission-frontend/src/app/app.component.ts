import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FormsModule } from '@angular/forms'; // For two-way binding
import { ApiService } from './services/api.service'; // Import your ApiService for backend interaction

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'ReMission - Your IBD Management Companion';
  userId: number | null = null;
  userIdInput: string = ''; // Store user input temporarily
  userIdError: string = ''; // Error message if user input fails validation

  constructor(private apiService: ApiService) {} // Inject ApiService

  ngOnInit(): void {
    // Prompt user for ID on load
    this.promptForUserId();
  }

  /**
   * Prompts the user to enter their User ID.
   */
  promptForUserId(): void {
    this.userId = null; // Ensure no userId is set on initial load
  }

  /**
   * Validates the entered User ID by checking against the backend.
   */
  confirmUserId(): void {
    if (this.userIdInput) {
      const inputId = parseInt(this.userIdInput, 10);

      this.apiService.validateUserId(inputId).subscribe(
        (response: any) => {
          this.userId = inputId;
          console.log(`User ID validated: ${this.userId}`);
        },
        (error: any) => {
          this.userIdError = 'Invalid User ID. Please try again.';
          console.error('Error validating User ID:', error);
        }
      );
    } else {
      this.userIdError = 'Please enter a valid User ID.';
    }
  }
}
