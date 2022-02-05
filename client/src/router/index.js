import Vue from 'vue';
import VueRouter from 'vue-router';
import CourseList from "../views/CourseList";
import UnitList from "../views/UnitList";
import LessonList from "../views/LessonList";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'CourseList',
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
  }
];

const router = new VueRouter({
  routes,
});

export default router;
