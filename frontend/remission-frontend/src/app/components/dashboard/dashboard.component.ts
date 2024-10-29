import { Component, OnInit } from '@angular/core';
import { Chart, registerables } from 'chart.js';
import { ApiService } from '../../services/api.service';

interface SymptomLog {
  logged_at: string;
  pain_level: number;
  stress_level: number;
  sleep_hours: number;
  exercise_done: boolean;
  took_medication: boolean;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  standalone: true,
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(private apiService: ApiService) {
    // Register Chart.js components
    Chart.register(...registerables);
  }

  ngOnInit(): void {
    this.fetchAndDisplayCharts();
  }

  fetchAndDisplayCharts(): void {
    this.apiService.getSymptomLogs().subscribe(
      (data: SymptomLog[]) => {
        this.createSymptomTrendChart(data);
        this.createStressLevelChart(data);
        this.createPainExerciseChart(data);
      },
      (error: any) => {
        console.error('Error fetching symptom logs:', error);
      }
    );
  }

  createSymptomTrendChart(data: SymptomLog[]): void {
    const labels = data.map((entry: SymptomLog) => new Date(entry.logged_at).toLocaleDateString());
    const symptomSeverity = data.map((entry: SymptomLog) => entry.pain_level);

    new Chart("symptomTrendChart", {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Symptom Severity',
          data: symptomSeverity,
          fill: false,
          borderColor: 'rgba(75, 192, 192, 1)',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
        }
      }
    });
  }

  createStressLevelChart(data: SymptomLog[]): void {
    const labels = data.map((entry: SymptomLog) => new Date(entry.logged_at).toLocaleDateString());
    const stressLevels = data.map((entry: SymptomLog) => entry.stress_level);

    new Chart("stressLevelChart", {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Stress Level',
          data: stressLevels,
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
        }
      }
    });
  }

  createPainExerciseChart(data: SymptomLog[]): void {
    const highPainNoExercise = data.filter((entry: SymptomLog) => entry.pain_level > 7 && !entry.exercise_done).length;
    const highPainExercise = data.filter((entry: SymptomLog) => entry.pain_level > 7 && entry.exercise_done).length;
    const lowPainNoExercise = data.filter((entry: SymptomLog) => entry.pain_level <= 7 && !entry.exercise_done).length;
    const lowPainExercise = data.filter((entry: SymptomLog) => entry.pain_level <= 7 && entry.exercise_done).length;

    new Chart("painExerciseChart", {
      type: 'doughnut',
      data: {
        labels: ['Pain High with No Exercise', 'Pain High with Exercise', 'Pain Low with No Exercise', 'Pain Low with Exercise'],
        datasets: [{
          label: 'Pain vs Exercise',
          data: [highPainNoExercise, highPainExercise, lowPainNoExercise, lowPainExercise],
          backgroundColor: [
            'rgba(255, 159, 64, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)'
          ],
          borderColor: [
            'rgba(255, 159, 64, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
        }
      }
    });
  }
}
