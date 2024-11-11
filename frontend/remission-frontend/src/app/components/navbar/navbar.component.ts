import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // Import RouterModule for navigation

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  standalone: true,
  styleUrls: ['./navbar.component.css'],
  imports: [CommonModule, RouterModule] // Ensure RouterModule is imported
})
export class NavbarComponent {}
