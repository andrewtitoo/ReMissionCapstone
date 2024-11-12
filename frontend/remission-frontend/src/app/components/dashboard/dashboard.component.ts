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
  exercise_done: boolean;
  took_medication: boolean;
  flare_up: number; // 1 for flare-up, 0 for no flare
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  standalone: true,
  styleUrls: ['./dashboard.component.css'],
  imports: [CommonModule, HttpClientModule]
})
export class DashboardComponent implements OnInit {
  loading = true;
  errorMessage: string | null = null;

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
          this.createSymptomTrendChart(data);
          this.createFlareDistributionChart(data);
          this.createSymptomBreakdownChart(data);
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

  createSymptomTrendChart(data: SymptomLog[]): void {
    const labels = data.map(entry => new Date(entry.logged_at).toLocaleDateString());
    const painLevels = data.map(entry => entry.pain_level);
    const stressLevels = data.map(entry => entry.stress_level);

    new Chart('symptomTrendChart', {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Pain Level',
            data: painLevels,
            borderColor: '#ff6384',
            fill: false,
          },
          {
            label: 'Stress Level',
            data: stressLevels,
            borderColor: '#36a2eb',
            fill: false,
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Symptom Trends Over Time' }
        }
      }
    });
  }

  createFlareDistributionChart(data: SymptomLog[]): void {
    const flareCounts = [
      data.filter(entry => entry.flare_up === 1).length,
      data.filter(entry => entry.flare_up === 0).length
    ];

    new Chart('flareDistributionChart', {
      type: 'pie',
      data: {
        labels: ['Flare-Ups', 'No Flare-Ups'],
        datasets: [
          {
            data: flareCounts,
            backgroundColor: ['#ff6384', '#36a2eb']
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Flare-Up Distribution' }
        }
      }
    });
  }

  createSymptomBreakdownChart(data: SymptomLog[]): void {
    const avgSleep = data.reduce((sum, log) => sum + log.sleep_hours, 0) / data.length;
    const avgExercise = (data.filter(log => log.exercise_done).length / data.length) * 100;
    const avgMedication = (data.filter(log => log.took_medication).length / data.length) * 100;

    new Chart('symptomBreakdownChart', {
      type: 'bar',
      data: {
        labels: ['Avg Sleep Hours', 'Exercise Done (%)', 'Medication Taken (%)'],
        datasets: [
          {
            label: 'Symptom Averages',
            data: [avgSleep, avgExercise, avgMedication],
            backgroundColor: ['#ffcd56', '#4bc0c0', '#ff9f40']
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Symptom Breakdown by Category' }
        }
      }
    });
  }
}
