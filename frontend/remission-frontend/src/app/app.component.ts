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
  userId: number | null = null;
  userIdInput: string = '';
  userIdError: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.promptForUserId();
  }

  promptForUserId(): void {
    this.userId = null;
  }

  generateNewUserId(): void {
    this.apiService.createUser().subscribe(
      (response: any) => {
        this.userIdInput = response.user_id.toString();
        alert(`New User ID Generated: ${this.userIdInput}. Please save it!`);
      },
      (error: any) => {
        this.userIdError = 'Failed to generate User ID. Try again later.';
        console.error('Error creating User ID:', error);
      }
    );
  }

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
      this.userIdError = 'Please enter or generate a valid User ID.';
    }
  }
}
