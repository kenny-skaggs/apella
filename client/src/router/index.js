import Vue from 'vue';
import VueRouter from 'vue-router';
import CourseList from "../views/CourseList";
import UnitList from "../views/UnitList";
import LessonList from "../views/LessonList";
import Lesson from "../views/Lesson/LessonController";
import Login from "../views/Login";

Vue.use(VueRouter);

const routes = [
  {
    name: 'dashboard',
    path: '/',
    component: CourseList,
  },
  {
    name: 'course_detail',
    path: '/course/:courseId',
    component: UnitList,
    props: true
  },
  {
    name: 'unit_detail',
    path: '/unit/:unitId',
    component: LessonList,
    props: true
  },
  {
    name: 'lesson_detail',
    path: '/lesson/:lessonId',
    component: Lesson,
    props: true
  },
  {
    name: 'login',
    path: '/login',
    component: Login,
    props: true
  }
];

const router = new VueRouter({
  routes,
});

export default router;
