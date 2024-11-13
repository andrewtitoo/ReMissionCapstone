import { Component, OnInit } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

interface SymptomLog {
  logged_at: string;
  pain_level: number;
  stress_level: number;
  sleep_hours: number;
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
  avgPainLevel: number = 0; // Store calculated average pain level

  constructor(private apiService: ApiService) {
    Chart.register(...registerables);
  }

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

    this.fetchAndDisplayCharts(storedUserId);
  }

  fetchAndDisplayCharts(userId: string): void {
    this.apiService.getSymptomLogs(userId).subscribe(
      (data: SymptomLog[]) => {
        if (data.length > 0) {
          const last7Logs = data.slice(-7); // Focus on the latest 7 logs
          this.createSleepTrendChart(last7Logs);
          this.createStressTrendChart(last7Logs);
          this.calculateAveragePain(last7Logs);
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

  createSleepTrendChart(data: SymptomLog[]): void {
    const labels = data.map((entry) => new Date(entry.logged_at).toLocaleDateString());
    const sleepHours = data.map((entry) => entry.sleep_hours);

    new Chart('sleepTrendChart', {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Sleep Hours',
            data: sleepHours,
            borderColor: '#36a2eb',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Sleep Hours Trend (Last 7 Logs)' },
        },
      },
    });
  }

  createStressTrendChart(data: SymptomLog[]): void {
    const labels = data.map((entry) => new Date(entry.logged_at).toLocaleDateString());
    const stressLevels = data.map((entry) => entry.stress_level);

    new Chart('stressTrendChart', {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Stress Levels',
            data: stressLevels,
            backgroundColor: '#ff6384',
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Stress Levels Trend (Last 7 Logs)' },
        },
      },
    });
  }

  calculateAveragePain(data: SymptomLog[]): void {
    const totalPain = data.reduce((sum, log) => sum + log.pain_level, 0);
    this.avgPainLevel = parseFloat((totalPain / data.length).toFixed(1));
  }
}
