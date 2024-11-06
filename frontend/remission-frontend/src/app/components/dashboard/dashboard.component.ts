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
  loading: boolean = true;  // Loading indicator
  errorMessage: string | null = null;  // Error message for failed API calls

  constructor(private apiService: ApiService) {
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
    const symptomSeverity = data.map(entry => entry.pain_level);

    new Chart("symptomTrendChart", {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Symptom Severity',
          data: symptomSeverity,
          borderColor: '#3a6ea5',
          tension: 0.1,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Symptom Severity Over Time' }
        }
      }
    });
  }

  createStressLevelChart(data: SymptomLog[]): void {
    const labels = data.map(entry => new Date(entry.logged_at).toLocaleDateString());
    const stressLevels = data.map(entry => entry.stress_level);

    new Chart("stressLevelChart", {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Stress Level',
          data: stressLevels,
          backgroundColor: '#ffcc00',
          borderColor: '#ffab00',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Average Stress Levels' }
        }
      }
    });
  }

  createPainExerciseChart(data: SymptomLog[]): void {
    const highPainNoExercise = data.filter(entry => entry.pain_level > 7 && !entry.exercise_done).length;
    const highPainExercise = data.filter(entry => entry.pain_level > 7 && entry.exercise_done).length;
    const lowPainNoExercise = data.filter(entry => entry.pain_level <= 7 && !entry.exercise_done).length;
    const lowPainExercise = data.filter(entry => entry.pain_level <= 7 && entry.exercise_done).length;

    new Chart("painExerciseChart", {
      type: 'doughnut',
      data: {
        labels: [
          'Pain High with No Exercise',
          'Pain High with Exercise',
          'Pain Low with No Exercise',
          'Pain Low with Exercise'
        ],
        datasets: [{
          data: [highPainNoExercise, highPainExercise, lowPainNoExercise, lowPainExercise],
          backgroundColor: [
            '#ff7043',
            '#42a5f5',
            '#ffee58',
            '#66bb6a'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Pain Levels vs Exercise' }
        }
      }
    });
  }
}
