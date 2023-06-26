using EMS.Core.Model;
using Microsoft.AspNet.Identity.EntityFramework;
using System.Data.Entity;
using System.Linq;
using System;
using System.Threading.Tasks;

namespace EMS.Data.Identity
{

    public class DataContext : IdentityDbContext<User, IdentityRole, string, IdentityUserLogin
        , IdentityUserRole, IdentityUserClaim>
    {
        public DataContext() : base("name=aspnetrun_cs")
        {
            Database.SetInitializer(new AuthContextInitializer());
        }
        public DbSet<Department> Departments { get; set; }
        public DbSet<Evaluation> Evaluations { get; set; }
        public DbSet<TaskCriteria> TaskCriterias { get; set; }
        public DbSet<Core.Model.Task> Tasks { get; set; }
        public DbSet<Rating> Rating { get; set; }
        public static DataContext Create()
        {
            return new DataContext();
        }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            //modelBuilder.Entity<User>()
            //            .HasRequired<Department>(s => s.Department)
            //            .WithMany(g => g.Users)
            //            .HasForeignKey(s => s.DepartmentId)
            //            .WillCascadeOnDelete();

            //modelBuilder.Entity<Evaluation>()
            //            .HasRequired<User>(s => s.User)
            //            .WithMany(g => g.Evaluations)
            //            .HasForeignKey(s => s.UserId)
            //            .WillCascadeOnDelete();

            #region table naming conventions
            modelBuilder.Entity<User>().ToTable("Users");
            modelBuilder.Entity<IdentityRole>().ToTable("Roles");
            modelBuilder.Entity<IdentityUserRole>().ToTable("UsersInRoles");
            modelBuilder.Entity<IdentityUserClaim>().ToTable("UserClaims");
            modelBuilder.Entity<IdentityUserLogin>().ToTable("UserLogins");
            #endregion
        }

        public override async Task<int> SaveChangesAsync()
        {
            UpdateAuditEntities();
            return await base.SaveChangesAsync();
        }
        private void UpdateAuditEntities()
        {
            var modifiedEntries = ChangeTracker.Entries()
                .Where(x => x.Entity is BaseEntity && (x.State == EntityState.Added || x.State == EntityState.Modified));

            foreach (var entry in modifiedEntries)
            {
                var entity = (BaseEntity)entry.Entity;
                DateTime now = DateTime.UtcNow;

                if (entry.State == EntityState.Added)
                {
                    entity.CreatedDate = now;
                    entity.CreatedBy = entity?.CreatedBy;
                }
                else
                {
                    base.Entry(entity).Property(x => x.CreatedBy).IsModified = false;
                    base.Entry(entity).Property(x => x.CreatedDate).IsModified = false;
                }

                entity.UpdatedDate = now;
            }
        }

    }


    public class AuthContextInitializer : DropCreateDatabaseIfModelChanges<DataContext>
    {
        protected override void Seed(DataContext context)
        {
            base.Seed(context);

            Identity.Seed.Init(context);
        }
    }
}