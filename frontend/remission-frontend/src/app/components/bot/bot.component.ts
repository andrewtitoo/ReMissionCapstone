import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule, NgClass } from '@angular/common'; // Combined imports
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  standalone: true,
  styleUrls: ['./bot.component.css'],
  imports: [CommonModule, NgClass, FormsModule] // Ensure CommonModule is included
})
export class BotComponent implements OnInit {
  messages: string[] = [];
  userMessage: string = '';  // Track user input for the chat

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.sendInitialInsights();
  }

  sendInitialInsights(): void {
    this.apiService.getBotAnalysis().subscribe(
      (data) => {
        if (data && data.analysis_summary) {
          this.messages.push('Hello! I am CHIIP, your companion for IBD management. Here are some insights based on your latest symptom data:');
          this.messages.push(data.analysis_summary);
        } else {
          this.messages.push('No recent insights available at the moment. Please log some symptoms for more detailed analysis.');
        }
      },
      (error) => {
        console.error('Error fetching insights from CHIIP:', error);
        this.messages.push('An error occurred while fetching insights. Please try again later.');
      }
    );
  }

  sendMessage(): void {
    if (this.userMessage.trim() !== '') {
      this.messages.push(this.userMessage);  // Display user message
      this.apiService.getBotResponse(this.userMessage).subscribe(
        (data) => {
          if (data && data.response) {
            this.messages.push(data.response);  // Display CHIIP's response
          } else {
            this.messages.push('I am here to help. Please log symptoms or ask me about IBD management!');
          }
        },
        (error) => {
          console.error('Error fetching response from CHIIP:', error);
          this.messages.push('An error occurred while fetching the response. Please try again later.');
        }
      );
      this.userMessage = '';  // Clear input after sending
    }
  }
}
