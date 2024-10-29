import { Component } from '@angular/core';

@Component({
  selector: 'app-logger',
  templateUrl: './logger.component.html',
  standalone: true,
  styleUrls: ['./logger.component.css']
})
export class LoggerComponent {
  // Form fields
  painLevel: number = 5;
  stressLevel: number = 5;
  sleepHours: number = 7;
  exerciseDone: boolean = false;
  tookMedication: boolean = false;

  // Exercise types
  exerciseTypes = [
    { name: 'Cardio', selected: false },
    { name: 'Strength', selected: false },
    { name: 'Yoga', selected: false },
    { name: 'Walking', selected: false }
  ];

  constructor() {}

  onSubmit(): void {
    const loggedData = {
      painLevel: this.painLevel,
      stressLevel: this.stressLevel,
      sleepHours: this.sleepHours,
      exerciseDone: this.exerciseDone,
      exerciseTypes: this.exerciseTypes.filter(e => e.selected).map(e => e.name),
      tookMedication: this.tookMedication
    };

    console.log('Logged Data:', loggedData);
    // Placeholder: Here you would make a request to the backend to save the logged data
    alert('Your symptoms have been logged successfully!');
  }
}
