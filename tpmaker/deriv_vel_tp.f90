      SUBROUTINE DERIV_VEL()
      use dimensiones
      use derivtools
      use velocidades
      use derivvel
      use consderper
      use consdernper
      use deltas
      IMPLICIT NONE
      integer i,j,k,l,m



!     VELOCIDADES

      DO k=1,nz
       DO j=1,ny
        DO i=1,nx
         du(i)=u(i,j,k)
        ENDDO
        call derivnper(nx,du,axnp,bxnp,cxnp,deltax)
        DO i=1,nx
         dvel(i,j,k,1)=du(i)
        ENDDO
       END DO
      END DO

      DO k=1,nz
       DO j=1,ny
        DO i=1,nx
         du(i)=v(i,j,k)
        ENDDO
        call derivnper(nx,du,axnp,bxnp,cxnp,deltax)
        DO i=1,nx
         dvel(i,j,k,4)=du(i)
        ENDDO
       END DO
      END DO

      DO k=1,nz
       DO j=1,ny
        DO i=1,nx
         du(i)=w(i,j,k)
        ENDDO
        call derivnper(nx,du,axnp,bxnp,cxnp,deltax)
        DO i=1,nx
         dvel(i,j,k,7)=du(i)
        ENDDO
       END DO
      END DO

      DO k=1,nz
       DO i=1,nx
        DO j=1,ny
         dv(j)=u(i,j,k)
        ENDDO
        call derivnper(ny,dv,aynp,bynp,cynp,deltay)
        DO j=1,ny
         dvel(i,j,k,2)=dv(j)
        ENDDO
       END DO
      END DO

      DO k=1,nz
       DO i=1,nx
        DO j=1,ny
         dv(j)=v(i,j,k)
        ENDDO
        call derivnper(ny,dv,aynp,bynp,cynp,deltay)
        DO j=1,ny
         dvel(i,j,k,5)=dv(j)
        ENDDO
       END DO
      END DO

      DO k=1,nz
       DO i=1,nx
        DO j=1,ny
         dv(j)=w(i,j,k)
        ENDDO
        call derivnper(ny,dv,aynp,bynp,cynp,deltay)
        DO j=1,ny
         dvel(i,j,k,8)=dv(j)
        ENDDO
       END DO
      END DO

      DO j=1,ny
       DO i=1,nx
        DO k=1,nz
         dw(k)=u(i,j,k)
        ENDDO
        call derivnper(nz,dw,aznp,bznp,cznp,deltaz)
        DO k=1,nz
         dvel(i,j,k,3)=dw(k)
        ENDDO
       END DO
      END DO

      DO j=1,ny
       DO i=1,nx
        DO k=1,nz
         dw(k)=v(i,j,k)
        ENDDO
        call derivnper(nz,dw,aznp,bznp,cznp,deltaz)
        DO k=1,nz
         dvel(i,j,k,6)=dw(k)
        ENDDO
       END DO
      END DO

      DO j=1,ny
       DO i=1,nx
        DO k=1,nz
         dw(k)=w(i,j,k)
        ENDDO
        call derivnper(nz,dw,aznp,bznp,cznp,deltaz)
        DO k=1,nz
         dvel(i,j,k,9)=dw(k)
        ENDDO
       END DO
      END DO


      return
      end subroutine deriv_vel
