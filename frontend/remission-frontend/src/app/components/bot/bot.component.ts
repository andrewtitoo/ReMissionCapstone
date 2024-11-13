import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  standalone: true,
  styleUrls: ['./bot.component.css'],
  imports: [CommonModule, HttpClientModule]
})
export class BotComponent implements OnInit {
  messages: string[] = [];

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
          this.messages.push(`Hey there! Here's what I've noticed about your symptoms:`);
          data.insights.forEach((insight) => this.messages.push(insight));
        } else {
          this.messages.push("Hmm, I don't see much recent data. Let's start logging!");
        }
      },
      () => this.messages.push("Oops! I had trouble fetching your data. Try again later?")
    );
  }
}
