import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

interface SymptomLog {
  logged_at: string;
  pain_level: number;
  stress_level: number;
  sleep_hours: number;
  flare_up: boolean;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  standalone: true,
  styleUrls: ['./dashboard.component.css'],
  imports: [CommonModule, HttpClientModule],
})
export class DashboardComponent implements OnInit {
  loading = true;
  errorMessage: string | null = null;
  symptomLogs: SymptomLog[] = [];
  avgPainLevel: number = 0;
  avgStressLevel: number = 0;
  avgSleepHours: number = 0;
  insights: string[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.initializeAndFetchData();
  }

  initializeAndFetchData(): void {
    const storedUserId = localStorage.getItem('user_id');
    if (!storedUserId) {
      this.errorMessage = 'User ID not found. Please refresh the app.';
      this.loading = false;
      return;
    }

    this.fetchData(storedUserId);
  }

  fetchData(userId: string): void {
    this.apiService.getSymptomLogs(userId).subscribe(
      (data: SymptomLog[]) => {
        if (data.length > 0) {
          this.symptomLogs = data;
          this.calculateAverages();
          this.generateInsights();
        } else {
          this.errorMessage = 'No data available to display.';
        }
        this.loading = false;
      },
      (error: any) => {
        console.error('Error fetching symptom logs:', error);
        this.errorMessage = 'Failed to load data. Please try again later.';
        this.loading = false;
      }
    );
  }

  calculateAverages(): void {
    const totalPain = this.symptomLogs.reduce((sum, log) => sum + log.pain_level, 0);
    const totalStress = this.symptomLogs.reduce((sum, log) => sum + log.stress_level, 0);
    const totalSleep = this.symptomLogs.reduce((sum, log) => sum + log.sleep_hours, 0);

    this.avgPainLevel = parseFloat((totalPain / this.symptomLogs.length).toFixed(1));
    this.avgStressLevel = parseFloat((totalStress / this.symptomLogs.length).toFixed(1));
    this.avgSleepHours = parseFloat((totalSleep / this.symptomLogs.length).toFixed(1));
  }

  generateInsights(): void {
    const latestLog = this.symptomLogs[0];
    if (latestLog.flare_up) {
      this.insights.push("Recent log indicates a potential flare-up. Review your symptoms carefully.");
    } else {
      this.insights.push("You're doing great! No recent signs of flare-up.");
    }

    if (this.avgSleepHours < 7) {
      this.insights.push("Your average sleep is below 7 hours. Aim for better rest.");
    }
    if (this.avgStressLevel > 6) {
      this.insights.push("Your stress levels are relatively high. Consider stress-reducing activities.");
    }
  }
}
