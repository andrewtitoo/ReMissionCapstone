import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule, NgClass } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  standalone: true,
  styleUrls: ['./bot.component.css'],
  imports: [CommonModule, NgClass, FormsModule, HttpClientModule]
})
export class BotComponent implements OnInit {
  messages: string[] = [];
  userMessage: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.sendInitialInsights();
  }

  sendInitialInsights(): void {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      this.messages.push("CHIIP: Uh-oh! I can't seem to find your User ID. Try refreshing?");
      return;
    }

    this.apiService.getBotAnalysis(userId).subscribe(
      (data: { classification: string; insights: string[] }) => {
        if (data.insights && data.insights.length > 0) {
          this.messages.push(`CHIIP: Hey there! Here's what I've noticed about your symptoms:`);
          data.insights.forEach((insight) => this.messages.push(insight));
        } else {
          this.messages.push("CHIIP: Hmm, I don't see much recent data. Let's start logging!");
        }
      },
      () => this.messages.push("CHIIP: Oops! I had trouble fetching your data. Try again later?")
    );
  }

  sendMessage(): void {
    if (this.userMessage.trim()) {
      this.messages.push(`You: ${this.userMessage}`);

      this.apiService.getBotResponse(this.userMessage).subscribe(
        (data: { response?: string }) => {
          this.messages.push(`CHIIP: ${data.response || "I'm here to chat! What else is on your mind?"}`);
        },
        () => this.messages.push("CHIIP: Hmm, something went wrong. Let's try that again later?")
      );

      this.userMessage = '';
    }
  }
}
