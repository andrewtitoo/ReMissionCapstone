import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule, NgClass } from '@angular/common'; // Combined imports
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule

@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  standalone: true,
  styleUrls: ['./bot.component.css'],
  imports: [CommonModule, NgClass, FormsModule, HttpClientModule] // Ensure HttpClientModule is included
})
export class BotComponent implements OnInit {
  messages: string[] = [];
  userMessage: string = '';  // Track user input for the chat

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.sendInitialInsights(); // Fetch initial insights on component load
  }

  /**
   * Fetches initial insights from CHIIP based on the latest symptom data.
   */
  sendInitialInsights(): void {
    const userId = 1; // Hardcoded user ID for MVP

    this.apiService.getBotAnalysis(userId).subscribe(
      (data: { analysis_summary?: string }) => {
        if (data && data.analysis_summary) {
          this.messages.push('Hello! I am CHIIP, your companion for IBD management. Here are some insights based on your latest symptom data:');
          this.messages.push(data.analysis_summary);
        } else {
          this.messages.push('No recent insights available. Please log some symptoms for analysis.');
        }
      },
      (error: { message: string }) => {
        console.error('Error fetching insights from CHIIP:', error);
        this.messages.push('An error occurred while fetching insights. Please try again later.');
      }
    );
  }

  /**
   * Sends a user message to CHIIP and fetches a response.
   */
  sendMessage(): void {
    if (this.userMessage.trim() !== '') {
      this.messages.push(`You: ${this.userMessage}`);  // Display user message in the chat

      this.apiService.getBotResponse(this.userMessage).subscribe(
        (data: { response?: string }) => {
          if (data && data.response) {
            this.messages.push(`CHIIP: ${data.response}`);  // Display CHIIP's response
          } else {
            this.messages.push('CHIIP: I am here to help. Please log symptoms or ask me about IBD management!');
          }
        },
        (error: { message: string }) => {
          console.error('Error fetching response from CHIIP:', error);
          this.messages.push('An error occurred while fetching the response. Please try again later.');
        }
      );

      this.userMessage = '';  // Clear input after sending
    }
  }
}
