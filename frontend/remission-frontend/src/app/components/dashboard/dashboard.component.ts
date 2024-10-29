import { Component, OnInit } from '@angular/core';
import { Chart, registerables } from 'chart.js';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  standalone: true,
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor() {
    // Register Chart.js components
    Chart.register(...registerables);
  }

  ngOnInit(): void {
    this.createSymptomTrendChart();
    this.createStressLevelChart();
    this.createPainExerciseChart();
  }

  createSymptomTrendChart(): void {
    new Chart("symptomTrendChart", {
      type: 'line',
      data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
          label: 'Symptom Severity',
          data: [3, 5, 2, 4, 6, 1, 3],
          fill: false,
          borderColor: 'rgba(75, 192, 192, 1)',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }

  createStressLevelChart(): void {
    new Chart("stressLevelChart", {
      type: 'bar',
      data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
          label: 'Stress Level',
          data: [5, 6, 4, 7, 5, 6, 3],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }

  createPainExerciseChart(): void {
    new Chart("painExerciseChart", {
      type: 'doughnut',
      data: {
        labels: ['Pain High with No Exercise', 'Pain High with Exercise', 'Pain Low with No Exercise', 'Pain Low with Exercise'],
        datasets: [{
          label: 'Pain vs Exercise',
          data: [10, 20, 30, 40],
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
        maintainAspectRatio: false
      }
    });
  }
}
