import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-menu-principal',
  templateUrl: './menu-principal.component.html',
  styleUrls: ['./menu-principal.component.css']
})
export class MenuPrincipalComponent {
  constructor(private router: Router) {}

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }
}
