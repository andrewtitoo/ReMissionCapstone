import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-bot',
  templateUrl: './bot.component.html',
  standalone: true,
  styleUrls: ['./bot.component.css']
})
export class BotComponent implements OnInit {
  messages: string[] = [];

  constructor() {}

  ngOnInit(): void {
    // Start the conversation by sending default insights from CHIIP
    this.sendInitialInsights();
  }

  sendInitialInsights(): void {
    // Placeholder: Here we would actually connect to backend to get real insights.
    const insights = [
      'Hello! I am CHIIP, your companion for IBD management. Here are some insights based on your latest symptom data.',
      'It looks like your stress levels were higher than usual this week. Consider taking some time to relax and unwind.',
      'You have missed your medication 2 times this week. Consistency is key in managing IBD symptoms—try to set reminders if needed.',
      'On days when you exercised, your pain levels were generally lower. Keep up the great work with light exercise!'
    ];

    this.messages.push(...insights);
  }
}
