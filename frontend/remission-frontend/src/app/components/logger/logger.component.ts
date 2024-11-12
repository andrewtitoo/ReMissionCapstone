import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

interface ExerciseType {
  name: string;
  selected: boolean;
}

@Component({
  selector: 'app-logger',
  templateUrl: './logger.component.html',
  standalone: true,
  styleUrls: ['./logger.component.css'],
  imports: [FormsModule, CommonModule, HttpClientModule]
})
export class LoggerComponent {
  painLevel: number = 5;
  stressLevel: number = 5;
  sleepHours: number = 7;
  exerciseDone: boolean = false;
  tookMedication: boolean = false;
  successMessage: string = '';
  errorMessage: string = '';

  exerciseTypes: ExerciseType[] = [
    { name: 'Cardio', selected: false },
    { name: 'Strength', selected: false },
    { name: 'Yoga', selected: false },
    { name: 'Walking', selected: false }
  ];

  constructor(private apiService: ApiService) {}

  onSubmit(): void {
    if (!this.isFormValid()) return;

    const userId = localStorage.getItem('user_id'); // Retrieve user ID as string

    if (!userId) {
      this.errorMessage = 'User ID is missing. Please refresh the page or contact support.';
      return;
    }

    const loggedData = {
      pain_level: this.painLevel,
      stress_level: this.stressLevel,
      sleep_hours: this.sleepHours,
      exercise_done: this.exerciseDone,
      exercise_types: this.exerciseTypes.filter((e) => e.selected).map((e) => e.name),
      took_medication: this.tookMedication
    };

    this.apiService.logSymptoms(loggedData, userId).subscribe(
      () => {
        this.successMessage = 'Your symptoms have been logged successfully!';
        this.resetForm();
      },
      (error: any) => {
        console.error('Error logging symptoms:', error);
        this.errorMessage = 'An error occurred while logging your symptoms. Please try again later.';
      }
    );
  }

  isFormValid(): boolean {
    return this.painLevel > 0 && this.stressLevel > 0 && this.sleepHours >= 0;
  }

  getProgress(): number {
    let progress = 0;
    if (this.painLevel > 0) progress += 25;
    if (this.stressLevel > 0) progress += 25;
    if (this.sleepHours >= 0) progress += 25;
    if (this.exerciseDone) progress += 15;
    if (this.tookMedication) progress += 10;
    return progress;
  }

  resetForm(): void {
    this.painLevel = 5;
    this.stressLevel = 5;
    this.sleepHours = 7;
    this.exerciseDone = false;
    this.tookMedication = false;
    this.exerciseTypes.forEach((exercise: ExerciseType) => (exercise.selected = false));
    this.successMessage = '';
    this.errorMessage = '';
  }
}
