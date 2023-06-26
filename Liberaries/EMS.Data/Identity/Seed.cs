using Microsoft.AspNet.Identity.EntityFramework;



namespace EMS.Data.Identity
{
    public static class Seed
    {
        /// <summary>
        /// initialize Admin User data with associated Roles and AccessPaths
        /// </summary>
        /// <param name="context"></param>
        public static void Init(DataContext context)
        {
            context.Users.AddOrUpdateExtension(InitialData.GetAdminUsers());
            context.Roles.AddOrUpdateExtension(InitialData.GetRoles());
            context.Departments.AddOrUpdateExtension(InitialData.GetDepartments());
            context.Set<IdentityUserRole>().AddOrUpdateExtension(InitialData.GetUsersInRoles());
        }
    }
}