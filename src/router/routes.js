const routes = [
  {
    path: "/",
    component: () => import("../pages/IndexPage.vue"),
  },
  {
    path: "/profile",
    component: () => import("src/pages/ProfilePage.vue"),
    name: "Profile",
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
