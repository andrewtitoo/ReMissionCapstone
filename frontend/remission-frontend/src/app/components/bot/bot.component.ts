import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  standalone: true,
  styleUrls: ['./bot.component.css']
})
export class BotComponent implements OnInit {
  messages: string[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.sendInitialInsights();
  }

  sendInitialInsights(): void {
    // Connect to the backend to get real insights from CHIIP
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
}
